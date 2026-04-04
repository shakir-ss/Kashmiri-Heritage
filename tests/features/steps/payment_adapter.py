import re
import time
from playwright.sync_api import expect

class PaymentAdapter:
    @staticmethod
    def handle_gateway(context, provider="razorpay"):
        if provider == "razorpay":
            # Wait for the main Razorpay iframe
            context.page.wait_for_selector('iframe.razorpay-checkout-frame', state='visible', timeout=30000)
            print("DEBUG: Razorpay Adapter engaged.")
        elif provider == "mock":
            print("DEBUG: Using Mock Payment Bypass.")

    @staticmethod
    def complete_netbanking(context):
        """Encapsulates the flaky Netbanking flow"""
        from .cart_checkout_steps import find_and_click_in_frames
        
        # 1. Select Netbanking
        find_and_click_in_frames(context.page, "text", "Netbanking")
        
        # 2. Select Bank
        if not find_and_click_in_frames(context.page, "text", "HDFC"):
            find_and_click_in_frames(context.page, "text", "CANARA BANK")

        # 3. Handle the Popup/Gateway
        with context.browser_context.expect_page(timeout=10000) as popup_info:
            find_and_click_in_frames(context.page, "text", "Pay")
        
        bank_page = popup_info.value
        
        # Click Success on whatever page it appears
        for p in context.browser_context.pages:
            try:
                btn = p.get_by_role("button", name="Success", exact=False).first
                if btn.is_visible(timeout=5000):
                    btn.click()
                    break
            except: continue
        
        context.page.wait_for_timeout(5000)
