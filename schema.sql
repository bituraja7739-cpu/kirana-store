-- ====================================================
-- KiranaPro Database Schema for Supabase
-- Copy and paste this into Supabase SQL Editor and click RUN
-- ====================================================

-- 1. Create items table
CREATE TABLE IF NOT EXISTS public.items (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  category TEXT DEFAULT 'General',
  unit TEXT DEFAULT 'pcs',
  buy_price NUMERIC DEFAULT 0,
  sell_price NUMERIC DEFAULT 0,
  stock NUMERIC DEFAULT 0,
  min_stock NUMERIC DEFAULT 5,
  updated_at BIGINT DEFAULT 0
);

-- 2. Create sales table
CREATE TABLE IF NOT EXISTS public.sales (
  bill_no TEXT PRIMARY KEY,
  date TEXT NOT NULL,
  customer_name TEXT,
  customer_phone TEXT,
  payment_mode TEXT DEFAULT 'Cash',
  items JSONB,
  subtotal NUMERIC DEFAULT 0,
  discount NUMERIC DEFAULT 0,
  grand_total NUMERIC DEFAULT 0
);

-- 3. Create settings table
CREATE TABLE IF NOT EXISTS public.settings (
  id INT PRIMARY KEY DEFAULT 1,
  shop_name TEXT DEFAULT 'Kirana Store',
  phone TEXT,
  address TEXT
);

-- 4. Enable Row Level Security (RLS) & Allow Read/Write
ALTER TABLE public.items ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.sales ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.settings ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "Allow all on items" ON public.items;
CREATE POLICY "Allow all on items" ON public.items FOR ALL USING (true) WITH CHECK (true);

DROP POLICY IF EXISTS "Allow all on sales" ON public.sales;
CREATE POLICY "Allow all on sales" ON public.sales FOR ALL USING (true) WITH CHECK (true);

DROP POLICY IF EXISTS "Allow all on settings" ON public.settings;
CREATE POLICY "Allow all on settings" ON public.settings FOR ALL USING (true) WITH CHECK (true);

-- 5. Enable Supabase Realtime for instant updates on all devices
ALTER PUBLICATION supabase_realtime ADD TABLE public.items;
ALTER PUBLICATION supabase_realtime ADD TABLE public.sales;
