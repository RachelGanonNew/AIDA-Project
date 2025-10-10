#!/usr/bin/env python3
"""
Automated Demo Recording Script for AIDA
Uses Playwright to automate browser interactions and record video
"""

import asyncio
import time
import sys
import subprocess

try:
    from playwright.async_api import async_playwright
except ImportError:
    print("📦 Playwright not found. Installing...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "playwright"])
    subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])
    from playwright.async_api import async_playwright
    print("✅ Playwright installed successfully!")

import os

async def record_aida_demo():
    """Record automated demo of AIDA application"""
    
    # Create demo videos directory
    os.makedirs("demo_videos", exist_ok=True)
    
    async with async_playwright() as p:
        # Launch browser with video recording
        browser = await p.chromium.launch(
            headless=False,  # Show browser for recording
            args=['--start-maximized']
        )
        
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            record_video_dir="./demo_videos/",
            record_video_size={'width': 1920, 'height': 1080}
        )
        
        page = await context.new_page()
        
        print("🎬 Starting AIDA Demo Recording...")
        
        # Scene 1: Navigate to Dashboard
        print("📋 Scene 1: Loading Dashboard...")
        await page.goto('http://localhost:3000')
        await page.wait_for_load_state('networkidle')
        await asyncio.sleep(3)  # Let dashboard fully load
        
        # Hover over performance metrics
        await page.hover('[data-testid="performance-monitor"]')
        await asyncio.sleep(2)
        
        # Show WebSocket connection status
        await page.hover('[data-testid="websocket-status"]')
        await asyncio.sleep(2)
        
        # Hover over health cards
        health_cards = await page.query_selector_all('[data-testid="health-card"]')
        for card in health_cards:
            await card.hover()
            await asyncio.sleep(1)
        
        # Scroll to show all content
        await page.evaluate('window.scrollTo(0, document.body.scrollHeight/2)')
        await asyncio.sleep(2)
        await page.evaluate('window.scrollTo(0, 0)')
        await asyncio.sleep(1)
        
        # Scene 2: Proposal Analysis
        print("🤖 Scene 2: AI Proposal Analysis...")
        await page.click('text=Proposals')
        await page.wait_for_load_state('networkidle')
        await asyncio.sleep(2)
        
        # Click analyze new proposal
        await page.click('text=Analyze New Proposal')
        await asyncio.sleep(1)
        
        # Fill in proposal details
        proposal_text = """
        Title: Treasury Diversification Strategy
        
        Description: Allocate 20% of USDC holdings to DeFi protocols for yield generation. Strategy includes 10% to Aave lending pools, 5% to Compound governance tokens, and 5% to Uniswap liquidity positions. Expected annual yield: 8-12%. Risk level: Medium. Implementation timeline: 30 days. This will help generate passive income while maintaining liquidity for operational expenses.
        """
        
        await page.fill('[data-testid="proposal-title"]', 'Treasury Diversification Strategy')
        await page.fill('[data-testid="proposal-description"]', proposal_text)
        await asyncio.sleep(1)
        
        # Click analyze with AI
        await page.click('text=Analyze with AI')
        await asyncio.sleep(5)  # Wait for AI analysis
        
        # Scroll through results
        await page.evaluate('window.scrollTo(0, document.body.scrollHeight/2)')
        await asyncio.sleep(3)
        
        # Scene 3: Hathor Integration
        print("⚡ Scene 3: Hathor Network Integration...")
        await page.click('text=Hathor')
        await page.wait_for_load_state('networkidle')
        await asyncio.sleep(2)
        
        # Hover over network info
        await page.hover('[data-testid="network-info"]')
        await asyncio.sleep(2)
        
        # Hover over feeless transactions
        await page.hover('text=$0')
        await asyncio.sleep(2)
        
        # Show nano contracts
        await page.hover('[data-testid="nano-contracts"]')
        await asyncio.sleep(2)
        
        # Show EVM bridge
        await page.hover('[data-testid="evm-bridge"]')
        await asyncio.sleep(2)
        
        # Scene 4: Action Execution
        print("🚀 Scene 4: One-Click Execution...")
        await page.click('text=Proposals')
        await asyncio.sleep(1)
        
        # Click execute proposal
        await page.click('text=Execute Proposal')
        await asyncio.sleep(1)
        
        # Show execution dialog
        await page.hover('text=Estimated Cost: $0')
        await asyncio.sleep(2)
        
        # Click execute
        await page.click('text=Execute')
        await asyncio.sleep(3)  # Wait for execution
        
        # Scene 5: API Documentation
        print("📚 Scene 5: API Documentation...")
        await page.goto('http://localhost:8000/docs')
        await page.wait_for_load_state('networkidle')
        await asyncio.sleep(2)
        
        # Scroll through API docs
        await page.evaluate('window.scrollTo(0, document.body.scrollHeight/3)')
        await asyncio.sleep(2)
        
        # Expand an endpoint
        await page.click('.opblock-summary')
        await asyncio.sleep(2)
        
        # Final scene: Back to dashboard
        print("🏆 Final Scene: Dashboard Summary...")
        await page.goto('http://localhost:3000')
        await page.wait_for_load_state('networkidle')
        await asyncio.sleep(3)
        
        print("✅ Demo recording completed!")
        print("📹 Video saved to: ./demo_videos/")
        
        await context.close()
        await browser.close()

async def main():
    """Main function to run the demo"""
    try:
        await record_aida_demo()
        print("🎉 AIDA Demo Recording Successful!")
        print("📁 Check ./demo_videos/ folder for the recorded video")
    except Exception as e:
        print(f"❌ Error during recording: {e}")
        print("💡 Make sure AIDA is running on http://localhost:3000")

if __name__ == "__main__":
    asyncio.run(main())