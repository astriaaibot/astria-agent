-- ASTRIA DATABASE SCHEMA
-- Initialize 9 tables in Supabase
-- Run this SQL in Supabase SQL editor to set up the database

-- 1. CLIENTS TABLE
CREATE TABLE IF NOT EXISTS clients (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  business_name TEXT NOT NULL,
  contact_name TEXT,
  email TEXT,
  phone TEXT,
  category TEXT,
  service_area_cities TEXT[] DEFAULT ARRAY[]::TEXT[],
  service_area_zips TEXT[] DEFAULT ARRAY[]::TEXT[],
  icp_filters JSONB DEFAULT '{}'::JSONB,
  stripe_customer_id TEXT,
  stripe_subscription_id TEXT,
  subscription_status TEXT DEFAULT 'active',
  subscription_tier TEXT DEFAULT '$500',
  monthly_lead_target INTEGER DEFAULT 50,
  onboarding_stage TEXT DEFAULT 'discovery',
  launched_date TIMESTAMP,
  created_date TIMESTAMP DEFAULT NOW(),
  updated_date TIMESTAMP DEFAULT NOW()
);

-- 2. LEADS TABLE
CREATE TABLE IF NOT EXISTS leads (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  client_id UUID NOT NULL REFERENCES clients(id) ON DELETE CASCADE,
  business_name TEXT NOT NULL,
  phone TEXT,
  email TEXT,
  website TEXT,
  address TEXT,
  city TEXT,
  state TEXT,
  zip TEXT,
  google_rating FLOAT,
  review_count INTEGER DEFAULT 0,
  category TEXT,
  place_id TEXT,
  scraped_date DATE DEFAULT CURRENT_DATE,
  status TEXT DEFAULT 'new',
  score INTEGER,
  tier TEXT,
  score_reasoning TEXT,
  contacted_date TIMESTAMP,
  last_email_date TIMESTAMP,
  last_reply_date TIMESTAMP,
  created_date TIMESTAMP DEFAULT NOW(),
  updated_date TIMESTAMP DEFAULT NOW()
);

-- 3. LEAD_DETAILS TABLE
CREATE TABLE IF NOT EXISTS lead_details (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  lead_id UUID NOT NULL REFERENCES leads(id) ON DELETE CASCADE,
  services TEXT,
  service_area TEXT,
  usp TEXT,
  team TEXT,
  pain_points TEXT,
  personalization_hook TEXT,
  analyzed_date TIMESTAMP DEFAULT NOW(),
  created_date TIMESTAMP DEFAULT NOW()
);

-- 4. EMAIL_SEQUENCES TABLE
CREATE TABLE IF NOT EXISTS email_sequences (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  lead_id UUID NOT NULL REFERENCES leads(id) ON DELETE CASCADE,
  client_id UUID NOT NULL REFERENCES clients(id) ON DELETE CASCADE,
  subject TEXT NOT NULL,
  body TEXT NOT NULL,
  send_day INTEGER,
  status TEXT DEFAULT 'pending_review',
  created_date TIMESTAMP DEFAULT NOW(),
  sent_date TIMESTAMP,
  sent_from_account TEXT,
  open_count INTEGER DEFAULT 0,
  click_count INTEGER DEFAULT 0,
  updated_date TIMESTAMP DEFAULT NOW()
);

-- 5. REPLIES TABLE
CREATE TABLE IF NOT EXISTS replies (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  lead_id UUID NOT NULL REFERENCES leads(id) ON DELETE CASCADE,
  client_id UUID NOT NULL REFERENCES clients(id) ON DELETE CASCADE,
  email_id UUID REFERENCES email_sequences(id),
  reply_text TEXT NOT NULL,
  received_date TIMESTAMP DEFAULT NOW(),
  classification TEXT,
  confidence FLOAT,
  draft_response TEXT,
  action TEXT,
  escalate_to_human BOOLEAN DEFAULT FALSE,
  escalation_reason TEXT,
  response_sent BOOLEAN DEFAULT FALSE,
  response_sent_date TIMESTAMP,
  created_date TIMESTAMP DEFAULT NOW()
);

-- 6. OPPORTUNITIES TABLE
CREATE TABLE IF NOT EXISTS opportunities (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  lead_id UUID NOT NULL REFERENCES leads(id) ON DELETE CASCADE,
  client_id UUID NOT NULL REFERENCES clients(id) ON DELETE CASCADE,
  first_interested_date TIMESTAMP DEFAULT NOW(),
  booking_link_sent_date TIMESTAMP,
  appointment_booked BOOLEAN DEFAULT FALSE,
  appointment_date TIMESTAMP,
  appointment_time TIME,
  show_status TEXT DEFAULT 'scheduled',
  notes TEXT,
  created_date TIMESTAMP DEFAULT NOW(),
  updated_date TIMESTAMP DEFAULT NOW()
);

-- 7. ERRORS TABLE
CREATE TABLE IF NOT EXISTS errors (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  task_name TEXT,
  error_message TEXT,
  error_details JSONB,
  input_data JSONB,
  timestamp TIMESTAMP DEFAULT NOW(),
  resolved BOOLEAN DEFAULT FALSE,
  resolution_notes TEXT
);

-- 8. ACTIVITIES_LOG TABLE
CREATE TABLE IF NOT EXISTS activities_log (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  client_id UUID REFERENCES clients(id) ON DELETE CASCADE,
  lead_id UUID REFERENCES leads(id) ON DELETE CASCADE,
  activity_type TEXT,
  details JSONB,
  timestamp TIMESTAMP DEFAULT NOW()
);

-- 9. REPORTS TABLE
CREATE TABLE IF NOT EXISTS reports (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  client_id UUID NOT NULL REFERENCES clients(id) ON DELETE CASCADE,
  week_start DATE NOT NULL,
  week_end DATE NOT NULL,
  leads_scraped INTEGER DEFAULT 0,
  leads_scored_hot INTEGER DEFAULT 0,
  leads_scored_warm INTEGER DEFAULT 0,
  emails_sent INTEGER DEFAULT 0,
  replies_received INTEGER DEFAULT 0,
  replies_interested INTEGER DEFAULT 0,
  replies_questions INTEGER DEFAULT 0,
  replies_objections INTEGER DEFAULT 0,
  replies_not_interested INTEGER DEFAULT 0,
  appointments_booked INTEGER DEFAULT 0,
  open_rate FLOAT DEFAULT 0,
  reply_rate FLOAT DEFAULT 0,
  report_text TEXT,
  sent_date TIMESTAMP DEFAULT NOW(),
  created_date TIMESTAMP DEFAULT NOW()
);

-- INDEXES FOR PERFORMANCE
CREATE INDEX idx_leads_client_id ON leads(client_id);
CREATE INDEX idx_leads_status ON leads(status);
CREATE INDEX idx_leads_created_date ON leads(created_date);
CREATE INDEX idx_email_sequences_client_id ON email_sequences(client_id);
CREATE INDEX idx_email_sequences_status ON email_sequences(status);
CREATE INDEX idx_replies_lead_id ON replies(lead_id);
CREATE INDEX idx_replies_client_id ON replies(client_id);
CREATE INDEX idx_opportunities_client_id ON opportunities(client_id);
CREATE INDEX idx_activities_client_id ON activities_log(client_id);
CREATE INDEX idx_activities_activity_type ON activities_log(activity_type);

-- ENABLE ROW LEVEL SECURITY (optional)
-- ALTER TABLE clients ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE leads ENABLE ROW LEVEL SECURITY;
-- ... etc for other tables

-- INSERT TEST CLIENT (optional)
INSERT INTO clients (business_name, contact_name, email, phone, category, service_area_cities, subscription_tier)
VALUES (
  'Test HVAC Company',
  'John Smith',
  'john@testhvac.com',
  '555-1234',
  'HVAC',
  ARRAY['Fort Lauderdale', 'Pompano Beach', 'Coral Springs'],
  '$500'
) ON CONFLICT DO NOTHING;

-- Verify tables created
SELECT tablename FROM pg_tables WHERE schemaname = 'public' ORDER BY tablename;
