#!/usr/bin/env python3
"""
Farcaster Client - Helper library for posting, replying, and engaging on Farcaster

Usage:
    from farcaster_client import FarcasterClient
    
    fc = FarcasterClient(
        api_key="...",
        signer_uuid="...",
        fid=12345
    )
    
    # Post a cast
    fc.post_cast("Hello Farcaster 🚀", channel="dev")
    
    # Reply to a cast
    fc.reply("Great insight!", parent_hash="0x...")
    
    # Get mentions
    mentions = fc.get_mentions()
    
    # Like a cast
    fc.like("0x...")
"""

import os
import requests
from typing import Optional, Dict, List, Any
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FarcasterClient:
    """Client for Farcaster API via Neynar"""
    
    BASE_URL = "https://api.neynar.com/v2/farcaster"
    
    def __init__(self, api_key: str, signer_uuid: str, fid: int):
        """
        Initialize Farcaster client
        
        Args:
            api_key: Neynar API key
            signer_uuid: Signer UUID for posting
            fid: Your Farcaster ID
        """
        self.api_key = api_key
        self.signer_uuid = signer_uuid
        self.fid = fid
        self.headers = {"api_key": api_key}
    
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
            channel: Optional channel ID (dev, ai, base, etc.)
            image_url: Optional image URL to embed
            
        Returns:
            API response with cast hash
        """
        # Validate byte length
        byte_length = len(text.encode('utf-8'))
        if byte_length > 320:
            logger.error(f"Cast too long: {byte_length} bytes (max 320)")
            return {"success": False, "error": "Cast exceeds 320 byte limit"}
        
        body = {
            "signer_uuid": self.signer_uuid,
            "text": text,
        }
        
        if channel:
            body["channel_id"] = channel
        
        if image_url:
            body["embeds"] = [{"url": image_url}]
        
        response = requests.post(
            f"{self.BASE_URL}/cast",
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
    
    def reply(
        self,
        text: str,
        parent_hash: str,
        image_url: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Reply to a cast
        
        Args:
            text: Reply text (max 320 bytes)
            parent_hash: Hash of cast to reply to
            image_url: Optional image URL
            
        Returns:
            API response with reply cast hash
        """
        body = {
            "signer_uuid": self.signer_uuid,
            "text": text,
            "parent": parent_hash,
        }
        
        if image_url:
            body["embeds"] = [{"url": image_url}]
        
        response = requests.post(
            f"{self.BASE_URL}/cast",
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
    
    def thread(self, texts: List[str], channel: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Post a thread (multiple connected casts)
        
        Args:
            texts: List of cast texts in order
            channel: Optional channel for first cast
            
        Returns:
            List of responses for each cast
        """
        results = []
        parent_hash = None
        
        for i, text in enumerate(texts):
            if i == 0:
                # First cast
                result = self.post_cast(text, channel=channel)
            else:
                # Reply to previous
                if parent_hash:
                    result = self.reply(text, parent_hash=parent_hash)
                else:
                    logger.error("Failed to get parent hash for thread")
                    break
            
            results.append(result)
            
            # Get hash for next reply
            if result.get("success") and result.get("cast"):
                parent_hash = result["cast"]["hash"]
        
        return results
    
    def get_mentions(self, limit: int = 25) -> List[Dict[str, Any]]:
        """
        Fetch recent mentions of your account
        
        Args:
            limit: Number of mentions to fetch
            
        Returns:
            List of mentions
        """
        response = requests.get(
            f"{self.BASE_URL}/notifications",
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
    
    def get_feed(self, channel: Optional[str] = None, limit: int = 25) -> List[Dict[str, Any]]:
        """
        Get feed or channel feed
        
        Args:
            channel: Optional channel ID to fetch
            limit: Number of casts to fetch
            
        Returns:
            List of casts
        """
        if channel:
            endpoint = f"{self.BASE_URL}/feed/channel"
            params = {"channel_id": channel, "limit": limit}
        else:
            endpoint = f"{self.BASE_URL}/feed/home"
            params = {"fid": self.fid, "limit": limit}
        
        response = requests.get(
            endpoint,
            params=params,
            headers=self.headers,
            timeout=10,
        )
        
        result = response.json()
        casts = result.get("casts", [])
        
        logger.info(f"📰 Fetched {len(casts)} casts")
        return casts
    
    def like(self, cast_hash: str) -> Dict[str, Any]:
        """
        Like a cast
        
        Args:
            cast_hash: Hash of cast to like
            
        Returns:
            API response
        """
        return self._react(cast_hash, "like")
    
    def recast(self, cast_hash: str) -> Dict[str, Any]:
        """
        Recast (amplify) a cast
        
        Args:
            cast_hash: Hash of cast to recast
            
        Returns:
            API response
        """
        return self._react(cast_hash, "recast")
    
    def _react(self, cast_hash: str, reaction_type: str) -> Dict[str, Any]:
        """
        React to a cast (like or recast)
        
        Args:
            cast_hash: Hash of cast
            reaction_type: "like" or "recast"
            
        Returns:
            API response
        """
        body = {
            "signer_uuid": self.signer_uuid,
            "reaction_type": reaction_type,
            "target": cast_hash,
        }
        
        response = requests.post(
            f"{self.BASE_URL}/reaction",
            json=body,
            headers=self.headers,
            timeout=10,
        )
        
        result = response.json()
        
        if response.status_code == 200 and result.get("success"):
            emoji = "❤️" if reaction_type == "like" else "🔄"
            logger.info(f"✅ {emoji} {reaction_type.capitalize()}ed cast")
        else:
            logger.error(f"❌ Failed to {reaction_type}: {result}")
        
        return result
    
    def search_casts(self, query: str, limit: int = 25) -> List[Dict[str, Any]]:
        """
        Search for casts
        
        Args:
            query: Search term
            limit: Number of results
            
        Returns:
            List of matching casts
        """
        response = requests.get(
            f"{self.BASE_URL}/search/casts",
            params={"q": query, "limit": limit},
            headers=self.headers,
            timeout=10,
        )
        
        result = response.json()
        casts = result.get("casts", [])
        
        logger.info(f"🔍 Found {len(casts)} casts matching '{query}'")
        return casts
    
    def search_users(self, query: str, limit: int = 25) -> List[Dict[str, Any]]:
        """
        Search for users
        
        Args:
            query: Search term
            limit: Number of results
            
        Returns:
            List of matching users
        """
        response = requests.get(
            f"{self.BASE_URL}/search/users",
            params={"q": query, "limit": limit},
            headers=self.headers,
            timeout=10,
        )
        
        result = response.json()
        users = result.get("users", [])
        
        logger.info(f"👥 Found {len(users)} users matching '{query}'")
        return users
    
    def get_user(self, username: str) -> Optional[Dict[str, Any]]:
        """
        Look up a user by username
        
        Args:
            username: Username to look up
            
        Returns:
            User object or None if not found
        """
        response = requests.get(
            f"{self.BASE_URL}/user/by_username",
            params={"username": username},
            headers=self.headers,
            timeout=10,
        )
        
        result = response.json()
        
        if response.status_code == 200 and result.get("user"):
            logger.info(f"👤 Found user: @{username}")
            return result["user"]
        else:
            logger.warning(f"User not found: @{username}")
            return None
    
    def preview_cast(self, text: str) -> bool:
        """
        Preview cast without posting (check byte length)
        
        Args:
            text: Cast text to check
            
        Returns:
            True if valid, False if too long
        """
        byte_length = len(text.encode('utf-8'))
        is_valid = byte_length <= 320
        
        status = "✅" if is_valid else "❌"
        logger.info(f"{status} Cast preview: {byte_length} / 320 bytes")
        
        if not is_valid:
            logger.warning(f"Cast exceeds limit by {byte_length - 320} bytes")
        
        return is_valid


# Example usage
if __name__ == "__main__":
    # Initialize client from environment
    fc = FarcasterClient(
        api_key=os.getenv("FARCASTER_NEYNAR_API_KEY"),
        signer_uuid=os.getenv("FARCASTER_SIGNER_UUID"),
        fid=int(os.getenv("FARCASTER_FID")),
    )
    
    # Example: Post a cast
    # fc.post_cast("Hello Farcaster 🚀", channel="dev")
    
    # Example: Get mentions
    # mentions = fc.get_mentions()
    # for mention in mentions:
    #     print(f"@{mention['cast']['author']['username']}: {mention['cast']['text']}")
    
    # Example: Get /dev feed
    # casts = fc.get_feed(channel="dev", limit=10)
    # for cast in casts:
    #     print(f"@{cast['author']['username']}: {cast['text'][:50]}...")
    
    # Example: Post a thread
    # fc.thread([
    #     "Thread incoming 🧵",
    #     "Here's part 2 of the thread",
    #     "And here's part 3 wrapping up"
    # ], channel="dev")
    
    print("Farcaster client ready. See examples in __main__ block.")
