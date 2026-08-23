import json
import os

from dotenv import load_dotenv
from google import genai

from app.agent.tools import execute_tool
from app.agent.tool_schemas import TOOLS


load_dotenv()


class ParcelPilotAgent:

    def __init__(self):

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY not found in environment."
            )

        self.client = genai.Client(
            api_key=api_key
        )

        self.model = "gemini-3.6-flash"

        # Stores an action waiting for user confirmation.
        #
        # Example:
        #
        # {
        #     "type": "cancel_order",
        #     "order_id": "ORD-1001"
        # }
        self.pending_action = None

    # =========================================================
    # SYSTEM INSTRUCTION
    # =========================================================

    def _build_system_instruction(
        self,
        user_context
    ):

        return f"""
You are ParcelPilot Support Agent.

You help ParcelPilot customers and authorized
support staff answer questions using ONLY the
provided ParcelPilot data and documents.

USER CONTEXT:
{json.dumps(user_context, indent=2)}

IMPORTANT RULES:

1. Never invent information.

2. Use tools whenever the answer requires:
   - account information
   - order information
   - ticket information
   - policies
   - customer agreements
   - SOPs
   - product documentation
   - known issues

3. Customer-specific agreements override general
   ParcelPilot policies when they explicitly contain
   different terms.

4. Source precedence:

   Signed customer agreement
          >
   Current support policy
          >
   Current product documentation
          >
   Historical tickets

5. Historical ticket resolutions are context only.
   They may contain incorrect information.

6. Never use deprecated policies as the current rule.

7. If reliable sources conflict and the conflict
   cannot be resolved using source precedence,
   explain the conflict and recommend human verification.

8. Never expose another customer's private information.

9. Never claim that an action was performed unless
   the corresponding action tool returned success.

10. State-changing actions require explicit user
    confirmation.

11. If the user has not explicitly confirmed an action,
    use the appropriate prepare_* tool.

12. When information is missing or uncertain,
    say so clearly rather than guessing.

13. Give concise but useful answers.

14. If an action tool returns:
    requires_confirmation = true

    you must NOT perform the actual state-changing
    action yet.

    Ask the user for explicit confirmation.

15. Never treat the user's original request to perform
    an action as confirmation for the final state-changing
    operation.

16. Never bypass access-control rules.

17. Never retrieve, expose, modify, cancel, or escalate
    resources belonging to another customer account.

18. If a tool returns an access-denied or authorization
    error, report that access is denied and do not
    attempt to bypass the restriction.

19. Never claim that a tool succeeded when it returned
    success = false.

20. For state-changing operations, only the explicit
    confirmation handled by the application may authorize
    the final action. Do not interpret the original request
    as confirmation.
"""

    # =========================================================
    # TOOL DECLARATIONS
    # =========================================================

    def _tool_declarations(self):

        declarations = []

        for tool in TOOLS:

            declarations.append(
                {
                    "name": tool["name"],
                    "description": tool["description"],
                    "parameters": tool["parameters"]
                }
            )

        return declarations

    # =========================================================
    # CONFIRMATION DETECTION
    # =========================================================

    def _is_confirmation(self, message):

        normalized = message.strip().lower()

        confirmation_phrases = [
            "yes",
            "yes please",
            "yes, please",
            "confirm",
            "confirmed",
            "i confirm",
            "i confirmed",
            "proceed",
            "go ahead",
            "do it",
            "please do it",
            "please proceed",
            "proceed with it",
            "approve",
            "approved",
            "cancel it",
            "create it"
        ]

        # Exact match
        if normalized in confirmation_phrases:
            return True

        # Natural-language confirmations
        if normalized.startswith("yes "):
            return True

        if normalized.startswith("yes,"):
            return True

        if "i confirm" in normalized:
            return True

        if "please proceed" in normalized:
            return True

        if "go ahead" in normalized:
            return True

        return False

    # =========================================================
    # REJECTION DETECTION
    # =========================================================

    def _is_rejection(self, message):

        normalized = message.strip().lower()

        rejection_phrases = [
            "no",
            "no thanks",
            "no, thanks",
            "don't",
            "do not",
            "stop",
            "cancel",
            "never mind",
            "never mind.",
            "do not proceed",
            "don't proceed",
            "don't do it",
            "do not do it"
        ]

        # Exact match
        if normalized in rejection_phrases:
            return True

        # Natural-language rejection
        if normalized.startswith("no "):
            return True

        if normalized.startswith("no,"):
            return True

        if "do not proceed" in normalized:
            return True

        if "don't proceed" in normalized:
            return True

        if "don't do it" in normalized:
            return True

        return False

    # =========================================================
    # GEMINI ERROR HANDLING
    # =========================================================

    def _handle_gemini_error(self, error):

        error_text = str(error)

        # -----------------------------------------------------
        # QUOTA / RATE LIMIT
        # -----------------------------------------------------

        if (
            "429" in error_text
            or "RESOURCE_EXHAUSTED" in error_text
            or "quota" in error_text.lower()
        ):

            return {
                "success": False,
                "answer": (
                    "The AI service has temporarily reached "
                    "its request limit. Please try again "
                    "after the quota resets."
                ),
                "error": (
                    "Gemini API quota exceeded."
                ),
                "tool_history": []
            }

        # -----------------------------------------------------
        # AUTHENTICATION
        # -----------------------------------------------------

        if (
            "401" in error_text
            or "403" in error_text
            or "API key" in error_text
        ):

            return {
                "success": False,
                "answer": (
                    "The AI service authentication "
                    "configuration needs attention."
                ),
                "error": (
                    "Gemini API authentication error."
                ),
                "tool_history": []
            }

        # -----------------------------------------------------
        # GENERIC GEMINI ERROR
        # -----------------------------------------------------

        return {
            "success": False,
            "answer": (
                "I'm temporarily unable to process "
                "your request. Please try again later."
            ),
            "error": error_text,
            "tool_history": []
        }

    # =========================================================
    # EXECUTE PENDING ACTION
    # =========================================================

    def _execute_pending_action(
        self,
        user_context,
        tool_history
    ):

        if self.pending_action is None:

            return {
                "success": False,
                "error": "No pending action exists."
            }

        action = self.pending_action

        action_type = action.get("type")

        # =====================================================
        # CANCEL ORDER
        # =====================================================

        if action_type == "cancel_order":

            order_id = action.get("order_id")

            arguments = {
                "order_id": order_id,
                "confirmed": True
            }

            print(
                "\n[AGENT TOOL] cancel_order"
            )

            print(
                f"[ARGUMENTS] {arguments}"
            )

            result = execute_tool(
                tool_name="cancel_order",
                arguments=arguments,
                user_context=user_context
            )

            print(
                f"[TOOL RESULT] {result}"
            )

            tool_history.append(
                {
                    "tool": "cancel_order",
                    "arguments": arguments,
                    "result": result
                }
            )

            # Clear pending action ONLY if action succeeded
            if result.get("success"):

                self.pending_action = None

            return result

        # =====================================================
        # CREATE ESCALATION
        # =====================================================

        if action_type == "create_escalation":

            ticket_id = action.get("ticket_id")
            reason = action.get("reason")
            priority = action.get("priority")

            arguments = {
                "ticket_id": ticket_id,
                "reason": reason,
                "priority": priority,
                "confirmed": True
            }

            print(
                "\n[AGENT TOOL] create_escalation"
            )

            print(
                f"[ARGUMENTS] {arguments}"
            )

            result = execute_tool(
                tool_name="create_escalation",
                arguments=arguments,
                user_context=user_context
            )

            print(
                f"[TOOL RESULT] {result}"
            )

            tool_history.append(
                {
                    "tool": "create_escalation",
                    "arguments": arguments,
                    "result": result
                }
            )

            # Clear pending action ONLY if action succeeded
            if result.get("success"):

                self.pending_action = None

            return result

        # =====================================================
        # UNKNOWN ACTION
        # =====================================================

        return {
            "success": False,
            "error": (
                f"Unknown pending action type: "
                f"{action_type}"
            )
        }

    # =========================================================
    # CHAT
    # =========================================================

    def chat(
        self,
        message,
        user_context
    ):

        tool_history = []

        # =====================================================
        # VALIDATE BASIC USER CONTEXT
        # =====================================================

        if not isinstance(user_context, dict):

            return {
                "success": False,
                "answer": (
                    "Invalid user context."
                ),
                "error": (
                    "user_context must be a dictionary."
                ),
                "tool_history": []
            }

        # =====================================================
        # HANDLE EXISTING PENDING ACTION
        # =====================================================

        if self.pending_action is not None:

            # -------------------------------------------------
            # USER CONFIRMED
            # -------------------------------------------------

            if self._is_confirmation(message):

                result = self._execute_pending_action(
                    user_context=user_context,
                    tool_history=tool_history
                )

                if result.get("success"):

                    return {
                        "success": True,
                        "answer": result.get(
                            "message",
                            "The requested action was completed successfully."
                        ),
                        "tool_history": tool_history
                    }

                return {
                    "success": False,
                    "answer": result.get(
                        "error",
                        "The requested action could not be completed."
                    ),
                    "tool_history": tool_history
                }

            # -------------------------------------------------
            # USER REJECTED
            # -------------------------------------------------

            if self._is_rejection(message):

                self.pending_action = None

                return {
                    "success": True,
                    "answer": (
                        "Understood. I will not perform "
                        "the pending action."
                    ),
                    "tool_history": tool_history
                }

            # -------------------------------------------------
            # UNCLEAR RESPONSE
            # -------------------------------------------------

            return {
                "success": True,
                "answer": (
                    "I have a pending action waiting for "
                    "your confirmation. Please reply "
                    "'yes' to confirm or 'no' to cancel."
                ),
                "tool_history": tool_history
            }

        # =====================================================
        # NORMAL GEMINI TOOL-CALLING FLOW
        # =====================================================

        system_instruction = self._build_system_instruction(
            user_context
        )

        contents = [
            message
        ]

        max_iterations = 8

        for iteration in range(max_iterations):

            # -------------------------------------------------
            # CALL GEMINI SAFELY
            # -------------------------------------------------

            try:

                response = self.client.models.generate_content(
                    model=self.model,
                    contents=contents,
                    config={
                        "system_instruction": system_instruction,
                        "tools": [
                            {
                                "function_declarations":
                                    self._tool_declarations()
                            }
                        ]
                    }
                )

            except Exception as error:

                print(
                    f"\n[GEMINI ERROR] {error}"
                )

                return self._handle_gemini_error(
                    error
                )

            # -------------------------------------------------
            # SAFETY CHECK RESPONSE
            # -------------------------------------------------

            if not response.candidates:

                return {
                    "success": False,
                    "answer": (
                        "The AI service returned "
                        "an empty response."
                    ),
                    "error": (
                        "No response candidates returned "
                        "by Gemini."
                    ),
                    "tool_history": tool_history
                }

            candidate = response.candidates[0]

            if not candidate.content:

                return {
                    "success": False,
                    "answer": (
                        "The AI service returned "
                        "an invalid response."
                    ),
                    "error": (
                        "Gemini response content was empty."
                    ),
                    "tool_history": tool_history
                }

            # -------------------------------------------------
            # STORE MODEL RESPONSE
            # -------------------------------------------------

            contents.append(
                candidate.content
            )

            # -------------------------------------------------
            # CHECK FOR FUNCTION CALLS
            # -------------------------------------------------

            function_calls = []

            for part in candidate.content.parts:

                if getattr(part, "function_call", None):

                    function_calls.append(
                        part.function_call
                    )

            # -------------------------------------------------
            # NO TOOL CALL = FINAL ANSWER
            # -------------------------------------------------

            if not function_calls:

                return {
                    "success": True,
                    "answer": response.text,
                    "tool_history": tool_history
                }

            # -------------------------------------------------
            # EXECUTE REQUESTED TOOLS
            # -------------------------------------------------

            for function_call in function_calls:

                tool_name = function_call.name

                arguments = dict(
                    function_call.args
                )

                print(
                    f"\n[AGENT TOOL] {tool_name}"
                )

                print(
                    f"[ARGUMENTS] {arguments}"
                )

                # =================================================
                # SAFETY CHECK FOR STATE-CHANGING TOOLS
                # =================================================

                state_changing_tools = [
                    "cancel_order",
                    "create_escalation"
                ]

                if tool_name in state_changing_tools:

                    # Never allow Gemini to perform a
                    # state-changing action directly.
                    #
                    # Gemini must first call prepare_*.
                    # Final action can only happen through
                    # the explicit confirmation flow.
                    arguments["confirmed"] = False

                # -------------------------------------------------
                # EXECUTE TOOL
                # -------------------------------------------------

                try:

                    result = execute_tool(
                        tool_name=tool_name,
                        arguments=arguments,
                        user_context=user_context
                    )

                except Exception as error:

                    result = {
                        "success": False,
                        "error": str(error)
                    }

                print(
                    f"[TOOL RESULT] {result}"
                )

                tool_history.append(
                    {
                        "tool": tool_name,
                        "arguments": arguments,
                        "result": result
                    }
                )

                # =================================================
                # STORE PENDING ACTION
                # =================================================

                if (
                    result.get("success") is True
                    and result.get("requires_confirmation") is True
                    and result.get("action") is not None
                ):

                    self.pending_action = result.get(
                        "action"
                    )

                    print(
                        f"[PENDING ACTION] "
                        f"{self.pending_action}"
                    )

                    # -------------------------------------------------
                    # IMPORTANT:
                    # Do not allow Gemini to continue making tool
                    # calls after a confirmation-required action.
                    # -------------------------------------------------

                    return {
                        "success": True,
                        "answer": result.get(
                            "message",
                            "This action requires your confirmation."
                        ),
                        "tool_history": tool_history
                    }

                # -------------------------------------------------
                # SEND TOOL RESULT BACK TO GEMINI
                # -------------------------------------------------

                contents.append(
                    {
                        "role": "user",
                        "parts": [
                            {
                                "text": (
                                    f"Tool result from "
                                    f"{tool_name}:\n"
                                    f"{json.dumps(result, default=str)}"
                                )
                            }
                        ]
                    }
                )

        # =====================================================
        # MAX ITERATIONS REACHED
        # =====================================================

        return {
            "success": False,
            "answer": (
                "I was unable to complete the request "
                "within the allowed processing steps."
            ),
            "error": (
                "Agent reached the maximum number "
                "of tool-calling iterations."
            ),
            "tool_history": tool_history
        }