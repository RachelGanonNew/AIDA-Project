"""
WebSocket service for real-time updates
"""
from fastapi import WebSocket, WebSocketDisconnect
from typing import List, Dict
import json
import asyncio
import logging

logger = logging.getLogger(__name__)

class WebSocketManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.dao_subscriptions: Dict[str, List[WebSocket]] = {}
    
    async def connect(self, websocket: WebSocket, dao_address: str = None):
        await websocket.accept()
        self.active_connections.append(websocket)
        
        if dao_address:
            if dao_address not in self.dao_subscriptions:
                self.dao_subscriptions[dao_address] = []
            self.dao_subscriptions[dao_address].append(websocket)
        
        logger.info(f"WebSocket connected. Total connections: {len(self.active_connections)}")
    
    def disconnect(self, websocket: WebSocket, dao_address: str = None):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        
        if dao_address and dao_address in self.dao_subscriptions:
            if websocket in self.dao_subscriptions[dao_address]:
                self.dao_subscriptions[dao_address].remove(websocket)
        
        logger.info(f"WebSocket disconnected. Total connections: {len(self.active_connections)}")
    
    async def send_personal_message(self, message: str, websocket: WebSocket):
        try:
            await websocket.send_text(message)
        except Exception as e:
            logger.error(f"Error sending personal message: {e}")
    
    async def broadcast(self, message: str):
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception as e:
                logger.error(f"Error broadcasting message: {e}")
                disconnected.append(connection)
        
        # Clean up disconnected connections
        for conn in disconnected:
            if conn in self.active_connections:
                self.active_connections.remove(conn)
    
    async def broadcast_to_dao(self, dao_address: str, message: str):
        if dao_address not in self.dao_subscriptions:
            return
        
        disconnected = []
        for connection in self.dao_subscriptions[dao_address]:
            try:
                await connection.send_text(message)
            except Exception as e:
                logger.error(f"Error broadcasting to DAO {dao_address}: {e}")
                disconnected.append(connection)
        
        # Clean up disconnected connections
        for conn in disconnected:
            if conn in self.dao_subscriptions[dao_address]:
                self.dao_subscriptions[dao_address].remove(conn)
    
    async def send_dao_update(self, dao_address: str, update_type: str, data: dict):
        message = json.dumps({
            "type": update_type,
            "dao_address": dao_address,
            "data": data,
            "timestamp": asyncio.get_event_loop().time()
        })
        await self.broadcast_to_dao(dao_address, message)

# Global WebSocket manager instance
websocket_manager = WebSocketManager()

# Background task to simulate real-time updates
async def simulate_real_time_updates():
    """Simulate real-time DAO updates for demo purposes"""
    import random
    
    sample_dao = "0x1234567890123456789012345678901234567890"
    
    while True:
        try:
            # Simulate health score update
            health_update = {
                "overall_health_score": random.uniform(0.7, 0.95),
                "governance_score": random.uniform(0.6, 0.9),
                "financial_score": random.uniform(0.8, 0.95),
                "community_score": random.uniform(0.7, 0.9)
            }
            await websocket_manager.send_dao_update(sample_dao, "health_update", health_update)
            
            await asyncio.sleep(10)  # Update every 10 seconds
            
            # Simulate proposal update
            proposal_update = {
                "proposal_id": f"prop_{random.randint(1000, 9999)}",
                "status": random.choice(["active", "passed", "failed"]),
                "votes_for": random.randint(100, 1000),
                "votes_against": random.randint(50, 500)
            }
            await websocket_manager.send_dao_update(sample_dao, "proposal_update", proposal_update)
            
            await asyncio.sleep(15)  # Update every 15 seconds
            
        except Exception as e:
            logger.error(f"Error in real-time updates: {e}")
            await asyncio.sleep(5)