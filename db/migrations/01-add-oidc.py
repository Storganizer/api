#!/usr/bin/env python

"""
Database migration script to add OIDC support and personId ownership to all entities.

This script adds:
1. oidc_sub and email columns to person table
2. personId foreign key to location table
3. personId foreign key to location_type table
4. personId foreign key to item table

All new columns are nullable to maintain backward compatibility with existing data.
"""

import sys
import os

# Add parent directory to path to import from api module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from sqlalchemy import text
from model.connection import engine, session

def run_migration():
    print("Starting database migration for OIDC support...")
    
    try:
        # Migration queries
        migrations = [
            # Add oidc_sub and email to person table
            "ALTER TABLE person ADD COLUMN IF NOT EXISTS oidc_sub VARCHAR UNIQUE",
            "ALTER TABLE person ADD COLUMN IF NOT EXISTS email VARCHAR",
            "CREATE INDEX IF NOT EXISTS idx_person_oidc_sub ON person(oidc_sub)",
            
            # Add personId to location table
            "ALTER TABLE location ADD COLUMN IF NOT EXISTS \"personId\" INTEGER REFERENCES person(id) ON DELETE CASCADE",
            "CREATE INDEX IF NOT EXISTS idx_location_personId ON location(\"personId\")",
            
            # Add personId to location_type table
            "ALTER TABLE location_type ADD COLUMN IF NOT EXISTS \"personId\" INTEGER REFERENCES person(id) ON DELETE CASCADE",
            "CREATE INDEX IF NOT EXISTS idx_location_type_personId ON location_type(\"personId\")",
            
            # Add personId to item table
            "ALTER TABLE item ADD COLUMN IF NOT EXISTS \"personId\" INTEGER REFERENCES person(id) ON DELETE CASCADE",
            "CREATE INDEX IF NOT EXISTS idx_item_personId ON item(\"personId\")",
        ]
        
        # Execute each migration
        for migration in migrations:
            print(f"Executing: {migration}")
            session.execute(text(migration))
        
        # Commit all changes
        session.commit()
        print("\n✓ Database migration completed successfully!")
        print("\nNew columns added:")
        print("  - person.oidc_sub (for OIDC user mapping)")
        print("  - person.email (for user email storage)")
        print("  - location.personId (for location ownership)")
        print("  - location_type.personId (for location type ownership)")
        print("  - item.personId (for item ownership)")
        print("\nNote: All new columns are nullable for backward compatibility.")
        
    except Exception as e:
        session.rollback()
        print(f"\n✗ Migration failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    run_migration()
    sys.exit(0)
