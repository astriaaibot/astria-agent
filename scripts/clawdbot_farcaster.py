#!/usr/bin/env python3
"""
Clawdbot for Farcaster - AgentGolf promotion bot

Handles:
- Daily posts for AgentGolf recruitment
- Registration frames
- Engagement with mentions
- Integration with Supabase for tracking
"""

import os
import requests
import json
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ClawdbotFarcaster:
    """Clawdbot for Farcaster - AgentGolf promotion"""
    
    NEYNAR_BASE_URL = "https://api.neynar.com/v2/farcaster"
    
    def __init__(self, api_key: str, signer_uuid: str, fid: int):
        """
        Initialize Clawdbot
        
        Args:
            api_key: Neynar API key
            signer_uuid: Signer UUID for posting
            fid: Clawdbot's Farcaster ID
        """
        self.api_key = api_key
        self.signer_uuid = signer_uuid
        self.fid = fid
        self.headers = {"api_key": api_key}
    
    def post_recruitment(self, category: str, details: str) -> Dict[str, Any]:
        """
        Post recruitment message for AgentGolf
        
        Args:
            category: e.g., "Trading", "Content", "Dev Tools"
            details: What kind of agents we're looking for
            
        Returns:
            API response
        """
        text = f"""🤖 AgentGolf: {category}

We're looking for agents that:
{details}

Building one? Register → [link]
Competition: [DATE]

Who's in? 👇"""
        
        return self.post_cast(
            text=text,
            channel="dev"
        )
    
    def post_cast(
        self,
        text: str,
        channel: Optional[str] = None,
        image_url: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Post a cast to Farcaster
        
        Args:
            text: Cast text (max 320 bytes)
            channel: Optional channel ID
            image_url: Optional image URL
            
        Returns:
            API response
        """
        byte_length = len(text.encode('utf-8'))
        if byte_length > 320:
            logger.error(f"Cast too long: {byte_length} bytes")
            return {"success": False, "error": "Exceeds 320 byte limit"}
        
        body = {
            "signer_uuid": self.signer_uuid,
            "text": text,
        }
        
        if channel:
            body["channel_id"] = channel
        
        if image_url:
            body["embeds"] = [{"url": image_url}]
        
        response = requests.post(
            f"{self.NEYNAR_BASE_URL}/cast",
            json=body,
            headers=self.headers,
            timeout=10,
        )
        
        result = response.json()
        
        if response.status_code == 200 and result.get("success"):
            logger.info(f"✅ Cast posted: {result['cast']['hash']}")
        else:
            logger.error(f"❌ Failed to post: {result}")
        
        return result
    
    def reply_to_mention(
        self,
        parent_hash: str,
        text: str,
    ) -> Dict[str, Any]:
        """
        Reply to a mention
        
        Args:
            parent_hash: Hash of cast to reply to
            text: Reply text
            
        Returns:
            API response
        """
        body = {
            "signer_uuid": self.signer_uuid,
            "text": text,
            "parent": parent_hash,
        }
        
        response = requests.post(
            f"{self.NEYNAR_BASE_URL}/cast",
            json=body,
            headers=self.headers,
            timeout=10,
        )
        
        result = response.json()
        
        if response.status_code == 200 and result.get("success"):
            logger.info(f"✅ Reply posted: {result['cast']['hash']}")
        else:
            logger.error(f"❌ Failed to reply: {result}")
        
        return result
    
    def get_mentions(self, limit: int = 25) -> List[Dict[str, Any]]:
        """
        Get recent mentions of Clawdbot
        
        Args:
            limit: Number of mentions to fetch
            
        Returns:
            List of mentions
        """
        response = requests.get(
            f"{self.NEYNAR_BASE_URL}/notifications",
            params={
                "fid": self.fid,
                "filter_type": "mention",
                "limit": limit,
            },
            headers=self.headers,
            timeout=10,
        )
        
        result = response.json()
        notifications = result.get("notifications", [])
        
        logger.info(f"📬 Fetched {len(notifications)} mentions")
        return notifications
    
    def auto_reply_to_questions(self) -> int:
        """
        Auto-reply to common questions about AgentGolf
        
        Returns:
            Number of replies sent
        """
        mentions = self.get_mentions(limit=50)
        replies_sent = 0
        
        keywords = {
            "register": "To register, click the frame below or visit [registration link]. Takes 2 minutes.",
            "categories": "We're looking for agents in: Trading, Content, Dev Tools, and Other. Any category welcome!",
            "rules": "Judged on: Innovation, Execution, Impact. No UI required. Just build something real.",
            "date": "AgentGolf runs [EVENT DATES]. Register now → [link]",
            "prize": "Prize pool: [AMOUNT]. But really, the prize is building cool stuff and being part of the community.",
        }
        
        for mention in mentions:
            cast_text = mention["cast"]["text"].lower()
            parent_hash = mention["cast"]["hash"]
            username = mention["cast"]["author"]["username"]
            
            # Find matching keyword
            for keyword, response_text in keywords.items():
                if keyword in cast_text:
                    reply = f"@{username}\n\n{response_text}"
                    self.reply_to_mention(parent_hash, reply)
                    replies_sent += 1
                    break
        
        logger.info(f"📤 Sent {replies_sent} auto-replies")
        return replies_sent
    
    def post_daily_hype(self, day: str = None) -> Dict[str, Any]:
        """
        Post daily recruitment/hype message
        
        Args:
            day: "mon", "tue", "wed", "thu", "fri" (if None, picks based on today)
            
        Returns:
            API response
        """
        if day is None:
            day = datetime.now().strftime("%a").lower()[:3]
        
        daily_posts = {
            "mon": """🤖 AgentGolf This Week

Building an agent? Now's your moment.

Categories:
→ Trading bots
→ Content creators
→ Dev tools
→ Your weird idea

Register: [link]
When: [DATE]

What's your idea? 👇""",
            
            "tue": """✨ Success Stories

Last year, @alice built [agent name]
Now used by [X] people daily.

You could be next.

AgentGolf: [link]
Register now → """,
            
            "wed": """💡 You Don't Need:
❌ Fancy UI
❌ Perfect code
❌ Experience
❌ Team

You just need:
✅ An idea
✅ Something that works
✅ Willingness to build

That's it.

Register: [link]""",
            
            "thu": """🔍 The Best Agents Are Weird

Not "general purpose AI"
But "an AI that [very specific thing]"

If you have a weird, specific idea,
we want it.

Build it.

Register: [link]""",
            
            "fri": """🚀 Ping to Builders:

@alice @bob @carol @dave

You should enter AgentGolf.

No pressure. Just think you'd crush it.

[link]""",
        }
        
        text = daily_posts.get(day, daily_posts["mon"])
        return self.post_cast(text=text, channel="dev")
    
    def post_entry_spotlight(
        self,
        agent_name: str,
        builder_username: str,
        description: str,
    ) -> Dict[str, Any]:
        """
        Spotlight a specific agent entry
        
        Args:
            agent_name: Name of the agent
            builder_username: @username of builder
            description: What the agent does
            
        Returns:
            API response
        """
        text = f"""🎉 ENTRY SPOTLIGHT

{agent_name} by @{builder_username}
{description}

This is the creativity we're here for.

If you haven't registered → [link]"""
        
        return self.post_cast(text=text, channel="dev")
    
    def post_countdown(self, days_remaining: int) -> Dict[str, Any]:
        """
        Post event countdown
        
        Args:
            days_remaining: Days until event
            
        Returns:
            API response
        """
        text = f"""🔴 LIVE IN {days_remaining} DAYS

The agents are coming.
The ideas are ready.
The competition starts [DATE].

This is happening.

Register → [link]
"""
        
        return self.post_cast(text=text, channel="dev")
    
    def post_event_live(self) -> Dict[str, Any]:
        """
        Post "event is live" announcement
        
        Returns:
            API response
        """
        text = """⏰ IT'S TIME

AgentGolf is officially LIVE.

Check out all entries → [mini app link]
Vote for your favorites
Celebrate the builders

This is going to be wild 🔥"""
        
        return self.post_cast(text=text, channel="dev")
    
    def post_winner_announcement(
        self,
        winners: List[Dict[str, str]],
    ) -> Dict[str, Any]:
        """
        Announce competition winners
        
        Args:
            winners: List of dicts with 'name', 'builder', 'description'
            
        Returns:
            API response
        """
        winners_text = "\n".join([
            f"🏆 {w['name']} by @{w['builder']}"
            for w in winners
        ])
        
        text = f"""🏆 AGENTGOLF WINNERS

{winners_text}

Congrats to everyone who participated.
You all raised the bar.

What's next? 👇"""
        
        return self.post_cast(text=text, channel="dev")


# Example: Frame handlers (Flask)

def register_frame_initial():
    """Initial registration frame - ask for name"""
    return {
        "version": "vNext",
        "image": "https://example.com/agentgolf-register.png",
        "input": {"text": "Your name..."},
        "buttons": [{"label": "Next", "action": "post"}]
    }


def register_frame_email():
    """Second frame - ask for email"""
    return {
        "version": "vNext",
        "image": "https://example.com/agentgolf-register.png",
        "input": {"text": "Your email..."},
        "buttons": [
            {"label": "Back", "action": "post"},
            {"label": "Next", "action": "post"}
        ]
    }


def register_frame_idea():
    """Third frame - ask for agent idea"""
    return {
        "version": "vNext",
        "image": "https://example.com/agentgolf-register.png",
        "input": {"text": "What's your agent idea? (brief)..."},
        "buttons": [
            {"label": "Back", "action": "post"},
            {"label": "Submit", "action": "post"}
        ]
    }


def register_frame_confirmation():
    """Final frame - confirmation"""
    return {
        "version": "vNext",
        "image": "https://example.com/agentgolf-confirmed.png",
        "buttons": [
            {"label": "View All Entries", "action": "link", "target": "https://miniapp.example.com"},
            {"label": "Close", "action": "post"}
        ]
    }


# Example usage
if __name__ == "__main__":
    # Initialize
    bot = ClawdbotFarcaster(
        api_key=os.getenv("FARCASTER_NEYNAR_API_KEY"),
        signer_uuid=os.getenv("FARCASTER_SIGNER_UUID"),
        fid=int(os.getenv("CLAWDBOT_FID")),
    )
    
    # Example: Post daily hype
    # bot.post_daily_hype(day="mon")
    
    # Example: Spotlight an entry
    # bot.post_entry_spotlight(
    #     agent_name="TradeBot Pro",
    #     builder_username="alice",
    #     description="Analyzes market trends and executes trades"
    # )
    
    # Example: Auto-reply to questions
    # bot.auto_reply_to_questions()
    
    # Example: Post countdown
    # bot.post_countdown(days_remaining=7)
    
    print("Clawdbot ready. See examples in __main__ block.")
