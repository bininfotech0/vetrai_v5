#!/usr/bin/env python3
"""
VetrAI Platform - Database Schema Validation
Validates database schema, relationships, and data integrity
"""
import asyncio
import asyncpg
import psycopg2
from psycopg2.extras import RealDictCursor
import json
import sys
from typing import Dict, List, Any
from datetime import datetime

class DatabaseSchemaValidator:
    def __init__(self, 
                 host: str = "localhost",
                 port: int = 5432,
                 database: str = "vetrai_db", 
                 user: str = "vetrai",
                 password: str = "vetrai_password"):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.connection = None
        
    def connect(self):
        """Connect to PostgreSQL database"""
        try:
            self.connection = psycopg2.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password,
                cursor_factory=RealDictCursor
            )
            print(f"✅ Connected to database: {self.database}")
            return True
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            return False
    
    def validate_schema(self):
        """Run comprehensive database schema validation"""
        print("🗄️ Starting Database Schema Validation")
        print("=" * 60)
        
        if not self.connect():
            return False
            
        try:
            cursor = self.connection.cursor()
            
            # Test 1: Validate basic connectivity
            self.test_connectivity(cursor)
            
            # Test 2: Check required tables
            self.validate_tables(cursor)
            
            # Test 3: Check table schemas
            self.validate_table_schemas(cursor)
            
            # Test 4: Check indexes
            self.validate_indexes(cursor)
            
            # Test 5: Check foreign key constraints
            self.validate_foreign_keys(cursor)
            
            # Test 6: Check extensions (pgvector)
            self.validate_extensions(cursor)
            
            # Test 7: Validate sample data
            self.validate_sample_data(cursor)
            
            print("\n✨ Database Schema Validation Complete")
            return True
            
        except Exception as e:
            print(f"❌ Schema validation failed: {e}")
            return False
        finally:
            if self.connection:
                self.connection.close()
    
    def test_connectivity(self, cursor):
        """Test basic database connectivity"""
        print("\n📡 Testing Database Connectivity...")
        
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        print(f"✅ PostgreSQL Version: {version}")
        
        cursor.execute("SELECT current_database();")
        db_name = cursor.fetchone()[0]
        print(f"✅ Connected to database: {db_name}")
        
        cursor.execute("SELECT current_user;")
        user = cursor.fetchone()[0]
        print(f"✅ Connected as user: {user}")
    
    def validate_tables(self, cursor):
        """Validate required tables exist"""
        print("\n📋 Validating Required Tables...")
        
        required_tables = [
            'users',
            'organizations', 
            'api_keys',
            'subscriptions',
            'tickets',
            'themes',
            'notifications',
            'workflows',
            'workflow_executions'
        ]
        
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            AND table_type = 'BASE TABLE'
        """)
        
        existing_tables = {row['table_name'] for row in cursor.fetchall()}
        
        for table in required_tables:
            if table in existing_tables:
                print(f"✅ Table exists: {table}")
            else:
                print(f"❌ Missing table: {table}")
        
        # Show all existing tables
        print(f"\n📊 Found {len(existing_tables)} tables in database:")
        for table in sorted(existing_tables):
            print(f"   • {table}")
    
    def validate_table_schemas(self, cursor):
        """Validate table schemas and columns"""
        print("\n🏗️ Validating Table Schemas...")
        
        # Define expected schemas for key tables
        expected_schemas = {
            'users': [
                'id', 'email', 'first_name', 'last_name', 'password_hash',
                'role', 'organization_id', 'is_active', 'email_verified',
                'created_at', 'updated_at'
            ],
            'organizations': [
                'id', 'name', 'plan_type', 'settings', 'is_active',
                'created_at', 'updated_at'
            ],
            'api_keys': [
                'id', 'name', 'key_hash', 'permissions', 'organization_id',
                'created_by', 'last_used', 'expires_at', 'is_active',
                'created_at', 'updated_at'
            ]
        }
        
        for table_name, expected_columns in expected_schemas.items():
            cursor.execute("""
                SELECT column_name, data_type, is_nullable
                FROM information_schema.columns
                WHERE table_name = %s
                ORDER BY ordinal_position
            """, (table_name,))
            
            columns = cursor.fetchall()
            if not columns:
                print(f"❌ Table {table_name} not found")
                continue
                
            existing_columns = {col['column_name'] for col in columns}
            
            print(f"\n🔍 Checking table: {table_name}")
            for col in expected_columns:
                if col in existing_columns:
                    print(f"  ✅ {col}")
                else:
                    print(f"  ❌ Missing column: {col}")
            
            # Show extra columns
            extra_columns = existing_columns - set(expected_columns)
            if extra_columns:
                print(f"  ℹ️ Additional columns: {', '.join(extra_columns)}")
    
    def validate_indexes(self, cursor):
        """Validate database indexes"""
        print("\n📊 Validating Indexes...")
        
        cursor.execute("""
            SELECT 
                schemaname,
                tablename,
                indexname,
                indexdef
            FROM pg_indexes 
            WHERE schemaname = 'public'
            ORDER BY tablename, indexname
        """)
        
        indexes = cursor.fetchall()
        print(f"Found {len(indexes)} indexes:")
        
        for idx in indexes:
            print(f"  • {idx['tablename']}.{idx['indexname']}")
    
    def validate_foreign_keys(self, cursor):
        """Validate foreign key constraints"""
        print("\n🔗 Validating Foreign Key Constraints...")
        
        cursor.execute("""
            SELECT
                tc.table_name,
                tc.constraint_name,
                tc.constraint_type,
                kcu.column_name,
                ccu.table_name AS foreign_table_name,
                ccu.column_name AS foreign_column_name
            FROM information_schema.table_constraints AS tc
            JOIN information_schema.key_column_usage AS kcu
                ON tc.constraint_name = kcu.constraint_name
                AND tc.table_schema = kcu.table_schema
            JOIN information_schema.constraint_column_usage AS ccu
                ON ccu.constraint_name = tc.constraint_name
                AND ccu.table_schema = tc.table_schema
            WHERE tc.constraint_type = 'FOREIGN KEY'
                AND tc.table_schema = 'public'
        """)
        
        foreign_keys = cursor.fetchall()
        print(f"Found {len(foreign_keys)} foreign key constraints:")
        
        for fk in foreign_keys:
            print(f"  • {fk['table_name']}.{fk['column_name']} -> {fk['foreign_table_name']}.{fk['foreign_column_name']}")
    
    def validate_extensions(self, cursor):
        """Validate PostgreSQL extensions"""
        print("\n🔧 Validating PostgreSQL Extensions...")
        
        cursor.execute("SELECT extname FROM pg_extension;")
        extensions = [row['extname'] for row in cursor.fetchall()]
        
        required_extensions = ['vector']  # pgvector for AI embeddings
        
        for ext in extensions:
            status = "✅ Required" if ext in required_extensions else "ℹ️ Additional"
            print(f"  {status}: {ext}")
        
        for ext in required_extensions:
            if ext not in extensions:
                print(f"  ❌ Missing required extension: {ext}")
    
    def validate_sample_data(self, cursor):
        """Validate sample data and basic queries"""
        print("\n📊 Validating Sample Data...")
        
        # Check if we have any data
        tables_to_check = ['users', 'organizations', 'api_keys', 'tickets']
        
        for table in tables_to_check:
            try:
                cursor.execute(f"SELECT COUNT(*) as count FROM {table}")
                count = cursor.fetchone()['count']
                print(f"  • {table}: {count} records")
            except Exception as e:
                print(f"  ❌ Error checking {table}: {e}")
        
        # Test basic queries
        try:
            cursor.execute("""
                SELECT u.email, o.name as org_name 
                FROM users u 
                LEFT JOIN organizations o ON u.organization_id = o.id 
                LIMIT 5
            """)
            results = cursor.fetchall()
            print(f"  ✅ User-Organization join query successful ({len(results)} records)")
        except Exception as e:
            print(f"  ❌ Join query failed: {e}")

def main():
    """Main validation runner"""
    validator = DatabaseSchemaValidator()
    success = validator.validate_schema()
    
    if success:
        print("\n🎉 Database validation completed successfully!")
        return 0
    else:
        print("\n💥 Database validation failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())