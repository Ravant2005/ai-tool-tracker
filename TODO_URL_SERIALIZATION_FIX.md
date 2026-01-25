# URL Serialization Fix Todo List

## Current Issues
- GitHub Actions workflow failing with "Object of type Url is not JSON serializable" errors
- Database connection errors in Supabase operations

## Files to Fix

### 1. backend/database/models.py
- [ ] Remove HttpUrl imports and use str instead
- [ ] Add proper URL validation with field_validator
- [ ] Ensure datetime fields are properly handled

### 2. backend/database/connection.py  
- [ ] Fix insert_tool method to handle URL serialization
- [ ] Ensure datetime objects are converted to ISO strings
- [ ] Add proper error handling

### 3. backend/scheduler/daily_job.py
- [ ] Fix datetime handling in tool creation
- [ ] Ensure proper tool data structure before database insertion
- [ ] Add validation for URL fields

## Implementation Steps

1. Update Pydantic models to use str instead of HttpUrl
2. Add URL validation with field_validator
3. Fix database connection serialization issues
4. Update scheduler to handle datetime properly
5. Test the fixes with GitHub Actions

## Expected Outcome
- GitHub Actions workflow should succeed
- No more JSON serialization errors
- Tools should be properly saved to Supabase database