#!/usr/bin/env python3
"""
Database Initialization Script for VetrAI Platform
Creates necessary tables and schemas for all services
"""

import psycopg2
import sys
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Database connection parameters
DB_CONFIG = {
    'host': 'localhost',
    'port': '5432',
    'database': 'vetrai',
    'user': 'vetrai_user',
    'password': 'vetrai_pass'
}

def create_tables():
    """Create all necessary tables for the services"""
    
    print("🔧 Initializing VetrAI Database Schema...")
    print("=" * 50)
    
    try:
        # Connect to database
        conn = psycopg2.connect(**DB_CONFIG)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        print("✅ Connected to PostgreSQL database")
        
        # Auth Service Tables
        print("\n📋 Creating Auth Service tables...")
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            email VARCHAR(255) UNIQUE NOT NULL,
            username VARCHAR(100) UNIQUE,
            password_hash VARCHAR(255) NOT NULL,
            first_name VARCHAR(100),
            last_name VARCHAR(100),
            is_active BOOLEAN DEFAULT TRUE,
            is_verified BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE TABLE IF NOT EXISTS user_sessions (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
            session_token VARCHAR(255) UNIQUE NOT NULL,
            refresh_token VARCHAR(255) UNIQUE,
            expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
        """)
        print("  ✅ Users and sessions tables created")
        
        # Tenancy Service Tables  
        print("\n🏢 Creating Tenancy Service tables...")
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS tenants (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            subdomain VARCHAR(100) UNIQUE,
            domain VARCHAR(255),
            is_active BOOLEAN DEFAULT TRUE,
            plan VARCHAR(50) DEFAULT 'free',
            settings JSONB DEFAULT '{}',
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE TABLE IF NOT EXISTS tenant_users (
            id SERIAL PRIMARY KEY,
            tenant_id INTEGER REFERENCES tenants(id) ON DELETE CASCADE,
            user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
            role VARCHAR(50) DEFAULT 'member',
            permissions JSONB DEFAULT '{}',
            joined_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(tenant_id, user_id)
        );
        """)
        print("  ✅ Tenant management tables created")
        
        # API Keys Service Tables
        print("\n🔑 Creating API Keys Service tables...")
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS api_keys (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
            tenant_id INTEGER REFERENCES tenants(id) ON DELETE CASCADE,
            name VARCHAR(255) NOT NULL,
            key_hash VARCHAR(255) UNIQUE NOT NULL,
            key_prefix VARCHAR(20) NOT NULL,
            permissions JSONB DEFAULT '[]',
            is_active BOOLEAN DEFAULT TRUE,
            last_used_at TIMESTAMP WITH TIME ZONE,
            expires_at TIMESTAMP WITH TIME ZONE,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE TABLE IF NOT EXISTS api_key_usage (
            id SERIAL PRIMARY KEY,
            api_key_id INTEGER REFERENCES api_keys(id) ON DELETE CASCADE,
            endpoint VARCHAR(255),
            method VARCHAR(10),
            status_code INTEGER,
            response_time_ms INTEGER,
            requested_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
        """)
        print("  ✅ API keys and usage tracking tables created")
        
        # Billing Service Tables
        print("\n💳 Creating Billing Service tables...")
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS billing_accounts (
            id SERIAL PRIMARY KEY,
            tenant_id INTEGER REFERENCES tenants(id) ON DELETE CASCADE UNIQUE,
            plan_type VARCHAR(50) DEFAULT 'free',
            billing_cycle VARCHAR(20) DEFAULT 'monthly',
            payment_method JSONB,
            billing_address JSONB,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE TABLE IF NOT EXISTS invoices (
            id SERIAL PRIMARY KEY,
            billing_account_id INTEGER REFERENCES billing_accounts(id) ON DELETE CASCADE,
            invoice_number VARCHAR(100) UNIQUE NOT NULL,
            amount_cents INTEGER NOT NULL,
            currency VARCHAR(3) DEFAULT 'USD',
            status VARCHAR(20) DEFAULT 'pending',
            due_date DATE,
            paid_at TIMESTAMP WITH TIME ZONE,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
        """)
        print("  ✅ Billing and invoice tables created")
        
        # Support Service Tables
        print("\n🎧 Creating Support Service tables...")
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS support_tickets (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
            tenant_id INTEGER REFERENCES tenants(id) ON DELETE CASCADE,
            title VARCHAR(255) NOT NULL,
            description TEXT,
            status VARCHAR(20) DEFAULT 'open',
            priority VARCHAR(20) DEFAULT 'medium',
            category VARCHAR(50),
            assigned_to INTEGER,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE TABLE IF NOT EXISTS ticket_messages (
            id SERIAL PRIMARY KEY,
            ticket_id INTEGER REFERENCES support_tickets(id) ON DELETE CASCADE,
            user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
            message TEXT NOT NULL,
            is_internal BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
        """)
        print("  ✅ Support ticket tables created")
        
        # Themes Service Tables
        print("\n🎨 Creating Themes Service tables...")
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS themes (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            description TEXT,
            config JSONB NOT NULL,
            is_default BOOLEAN DEFAULT FALSE,
            is_custom BOOLEAN DEFAULT FALSE,
            tenant_id INTEGER REFERENCES tenants(id) ON DELETE CASCADE,
            created_by INTEGER REFERENCES users(id),
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE TABLE IF NOT EXISTS user_theme_preferences (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
            theme_id INTEGER REFERENCES themes(id) ON DELETE CASCADE,
            preferences JSONB DEFAULT '{}',
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(user_id, theme_id)
        );
        """)
        print("  ✅ Theme management tables created")
        
        # Notifications Service Tables
        print("\n🔔 Creating Notifications Service tables...")
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS notifications (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
            tenant_id INTEGER REFERENCES tenants(id) ON DELETE CASCADE,
            title VARCHAR(255) NOT NULL,
            message TEXT,
            type VARCHAR(50) DEFAULT 'info',
            channel VARCHAR(50) DEFAULT 'in_app',
            is_read BOOLEAN DEFAULT FALSE,
            metadata JSONB DEFAULT '{}',
            scheduled_at TIMESTAMP WITH TIME ZONE,
            sent_at TIMESTAMP WITH TIME ZONE,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE TABLE IF NOT EXISTS notification_preferences (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
            channel VARCHAR(50) NOT NULL,
            enabled BOOLEAN DEFAULT TRUE,
            settings JSONB DEFAULT '{}',
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(user_id, channel)
        );
        """)
        print("  ✅ Notification tables created")
        
        # Workers Service Tables
        print("\n⚙️ Creating Workers Service tables...")
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS background_jobs (
            id SERIAL PRIMARY KEY,
            job_type VARCHAR(100) NOT NULL,
            job_data JSONB NOT NULL,
            status VARCHAR(20) DEFAULT 'pending',
            priority INTEGER DEFAULT 0,
            max_retries INTEGER DEFAULT 3,
            retry_count INTEGER DEFAULT 0,
            result JSONB,
            error_message TEXT,
            scheduled_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            started_at TIMESTAMP WITH TIME ZONE,
            completed_at TIMESTAMP WITH TIME ZONE,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE TABLE IF NOT EXISTS workflow_executions (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
            tenant_id INTEGER REFERENCES tenants(id) ON DELETE CASCADE,
            workflow_name VARCHAR(255) NOT NULL,
            workflow_config JSONB NOT NULL,
            status VARCHAR(20) DEFAULT 'running',
            input_data JSONB,
            output_data JSONB,
            error_details TEXT,
            started_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMP WITH TIME ZONE
        );
        """)
        print("  ✅ Background job and workflow tables created")
        
        # Create indexes for better performance
        print("\n📈 Creating database indexes...")
        cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
        CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
        CREATE INDEX IF NOT EXISTS idx_tenant_users_tenant_id ON tenant_users(tenant_id);
        CREATE INDEX IF NOT EXISTS idx_api_keys_user_id ON api_keys(user_id);
        CREATE INDEX IF NOT EXISTS idx_api_keys_tenant_id ON api_keys(tenant_id);
        CREATE INDEX IF NOT EXISTS idx_support_tickets_user_id ON support_tickets(user_id);
        CREATE INDEX IF NOT EXISTS idx_notifications_user_id ON notifications(user_id);
        CREATE INDEX IF NOT EXISTS idx_background_jobs_status ON background_jobs(status);
        CREATE INDEX IF NOT EXISTS idx_workflow_executions_user_id ON workflow_executions(user_id);
        """)
        print("  ✅ Database indexes created")
        
        # Insert default data
        print("\n💾 Inserting default data...")
        
        # Default tenant
        cursor.execute("""
        INSERT INTO tenants (name, subdomain, plan) 
        VALUES ('VetrAI Demo', 'demo', 'enterprise') 
        ON CONFLICT (subdomain) DO NOTHING;
        """)
        
        # Default theme
        cursor.execute("""
        INSERT INTO themes (name, description, config, is_default) 
        VALUES (
            'Default Theme', 
            'VetrAI default theme configuration',
            '{"colors": {"primary": "#3B82F6", "secondary": "#10B981"}, "typography": {"fontFamily": "Inter"}}',
            true
        ) ON CONFLICT DO NOTHING;
        """)
        
        print("  ✅ Default data inserted")
        
        cursor.close()
        conn.close()
        
        print("\n🎉 Database initialization completed successfully!")
        print("📊 All service tables and indexes created")
        print("🚀 VetrAI platform is ready to use!")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Database initialization failed: {e}")
        return False

if __name__ == "__main__":
    success = create_tables()
    sys.exit(0 if success else 1)