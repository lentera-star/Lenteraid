-- Delete old "Sahabat Lentera" conversation and messages
-- Run this in Supabase SQL Editor

-- 1. Find and delete messages from old conversation
DELETE FROM messages 
WHERE conversation_id IN (
  SELECT id FROM conversations 
  WHERE title = 'Sahabat Lentera'
);

-- 2. Delete the old conversation
DELETE FROM conversations 
WHERE title = 'Sahabat Lentera';

-- Verify deletion
SELECT * FROM conversations WHERE title LIKE '%Lentera%';
