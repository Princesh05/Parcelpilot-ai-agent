class AccessControl:

    @staticmethod
    def can_access_account(user_context, account_id):
        """
        Determine whether the current user can access an account.
        """

        role = user_context.get("role")

        # Internal ParcelPilot support users
        # can access customer accounts.
        if role in ["support_agent", "admin"]:
            return True

        # Customers can only access their own account.
        if role == "customer":
            return user_context.get("account_id") == account_id

        return False