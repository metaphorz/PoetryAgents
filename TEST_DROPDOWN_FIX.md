# Test Instructions - Model Dropdown Fix

## 🧪 How to Test the Fix

### Step 1: Open the Interface
```bash
# Open in browser
open poetry_generator_live.html
# OR double-click the file
```

### Step 2: Check Debug Panel
- **Look for the debug panel** at the top of the page
- Should show: "Debug Output: Interface loading..."
- Watch for messages like:
  - "Model data loaded: YES"
  - "Direct API providers: Claude, Gemini, OpenAI"
  - "Claude: 6 models" (or similar counts)

### Step 3: Test Provider Selection
1. **Select "Claude"** for Poet 1
   - Debug panel should show: "Poet 1 provider changed to: Claude"
   - Model dropdown should **immediately populate** with options like:
     - Claude Sonnet 4
     - Claude Opus 4.1
     - Claude Haiku 3.5
     - etc.

2. **Select "OpenAI"** for Poet 2
   - Debug panel shows: "Poet 2 provider changed to: OpenAI" 
   - Model dropdown populates with:
     - GPT-4o
     - GPT-4o Mini
     - etc.

### Step 4: Test OpenRouter Mode
1. **Click "OpenRouter" radio button**
   - Direct API dropdowns should disappear
   - OpenRouter provider dropdowns appear
   
2. **Select "Anthropic"** for Poet 1
   - Model dropdown should populate with OpenRouter models
   - Debug shows: "Found X OpenRouter models for anthropic"

### Step 5: Generate Poetry
1. **Fill all required fields:**
   - Theme: "moonlit garden path"
   - Form: Haiku
   - Rounds: 2
   - Emojis: No

2. **Click "Generate Poetry Script"**
   - Should show download section
   - Debug shows: "Python script generated successfully"

## ✅ Success Criteria

**The fix is working if:**
- ✅ Debug panel shows model data loaded
- ✅ Provider selection immediately populates model dropdowns  
- ✅ Both Direct API and OpenRouter modes work
- ✅ Model options are visible (not empty dropdowns)
- ✅ Python script generation works

**If you see issues:**
- 🔍 Check browser console (F12 → Console) for errors
- 📋 Read debug panel messages for specific error details
- 🔄 Try refreshing the page and test again

## 🚨 Troubleshooting

### Empty Dropdowns
- Check debug panel for "ERROR: No models found"
- Model data might not be loading correctly

### JavaScript Errors
- Open browser console (F12)
- Look for red error messages
- Common issues: element not found, function undefined

### Debug Panel Not Showing
- Interface might not have deployed correctly
- Check if you're opening the right file (poetry_generator_live.html)

## 📞 Getting Help

If the fix doesn't work:
1. Check browser console for errors
2. Look at debug panel messages
3. Compare with poetry_generator_fixed.html (backup version)
4. Run: `./poetry_agents.sh --refresh` to regenerate

The debug panel provides real-time feedback on exactly what's happening!
