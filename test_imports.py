#!/usr/bin/env python3
"""Test script to verify all imports work correctly."""

try:
    print("Testing core imports...")
    from app.core.config import settings
    from app.core.database import init_db
    print("✓ Core imports successful")
    
    print("Testing model imports...")
    from app.models.user import User
    from app.models.transaction import Transaction
    print("✓ Model imports successful")
    
    print("Testing repository imports...")
    from app.repositories.base import BaseRepository
    from app.repositories.user import UserRepository
    from app.repositories.transaction import TransactionRepository
    print("✓ Repository imports successful")
    
    print("Testing service imports...")
    from app.services.auth import AuthService
    from app.services.transaction import TransactionService
    print("✓ Service imports successful")
    
    print("Testing router imports...")
    from app.routers.auth import router as auth_router
    from app.routers.transactions import router as transactions_router
    print("✓ Router imports successful")
    
    print("Testing main app import...")
    from app.main import app
    print("✓ Main app import successful")
    
    print("\n🎉 All imports successful! The application should start correctly now.")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    import traceback
    traceback.print_exc()
except Exception as e:
    print(f"❌ Unexpected error: {e}")
    import traceback
    traceback.print_exc()