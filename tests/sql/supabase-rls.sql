-- The policy from GHSA-8h52-3cfj-cmrw.
-- # ruleid: postgres-rls-policy-using-true-for-anon
CREATE POLICY "Allow public access to profiles"
ON public.profiles
FOR SELECT
TO anon, authenticated
USING (true);

-- The narrower policy that sat next to it. It does not limit the one above.
-- # ok: postgres-rls-policy-using-true-for-anon
CREATE POLICY "Public profiles are viewable"
ON public.profiles
FOR SELECT
TO anon
USING (public_access = true);

-- No TO clause means PUBLIC, which includes anon.
-- # ruleid: postgres-rls-policy-using-true-for-anon
create policy read_all on public.notes for select using ( true );

-- # ok: postgres-rls-policy-using-true-for-anon
CREATE POLICY "Users read own row" ON public.profiles FOR SELECT TO authenticated USING (true);

-- A restrictive policy can only narrow access.
-- # ok: postgres-rls-policy-using-true-for-anon
CREATE POLICY "tenant gate" ON public.items AS RESTRICTIVE FOR SELECT TO anon USING (true);

-- # ok: postgres-rls-policy-using-true-for-anon
CREATE POLICY "own rows" ON public.items FOR SELECT TO anon, authenticated USING (auth.uid() = owner_id);

-- # ruleid: postgres-rls-policy-with-check-true-for-anon
CREATE POLICY "Anyone can sign up" ON public.waitlist FOR INSERT TO anon WITH CHECK (true);

-- # ok: postgres-rls-policy-with-check-true-for-anon
CREATE POLICY "insert own" ON public.items FOR INSERT TO authenticated WITH CHECK (auth.uid() = owner_id);

-- # ruleid: postgres-rls-disabled
ALTER TABLE public.audit_log DISABLE ROW LEVEL SECURITY;

-- # ok: postgres-rls-disabled
ALTER TABLE public.audit_log ENABLE ROW LEVEL SECURITY;
