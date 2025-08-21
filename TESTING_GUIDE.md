# Testing Guide for Poetry Generator HTML Interface

## Quick Test Instructions

### 1. Open the HTML File
- Double-click `poetry_generator.html` 
- OR open in browser with Ctrl+O (Cmd+O on Mac)

### 2. Test Direct API Mode (Default)
The page should load with "Direct APIs" already selected.

**Test Provider Selection:**
1. **Poet 1**: Click the "LLM Provider" dropdown
   - Should see: Claude (Anthropic), Gemini (Google), OpenAI
   - Select "Claude (Anthropic)"
   - **Model dropdown should become enabled** and show:
     - Claude Sonnet 4
     - Claude Opus 4.1  
     - Claude Opus 4
     - Claude Sonnet 3.5 (Latest)
     - Claude Sonnet 3.5 (June)
     - Claude Haiku 3.5

2. **Poet 2**: Select a different provider (e.g., "OpenAI")
   - Model dropdown should show:
     - GPT-4o
     - GPT-4o Mini
     - GPT-4 Turbo
     - GPT-4
     - GPT-3.5 Turbo

### 3. Test OpenRouter Mode
1. Click the "OpenRouter" radio button at the top
2. **Direct provider dropdowns should disappear**
3. **Text input fields should appear** for both poets
4. Enter model names like:
   - Poet 1: `anthropic/claude-3.5-sonnet`
   - Poet 2: `openai/gpt-4o`

### 4. Test Form Generation
1. Enter a theme: `walking in autumn rain`
2. Select a poetry form: `Haiku` 
3. Select rounds: `2 Rounds`
4. Select emojis: `No emojis`
5. Click "**Generate Poetry Script**"
6. Should see download section appear
7. Click "**Download run_poetry.py**"
8. File should download to your Downloads folder

## What Should Happen

### ✅ Working Correctly
- Provider dropdowns populate model lists immediately
- Model dropdowns show 5-6 options per provider
- Switching API modes shows/hides appropriate fields
- Form generates and downloads Python script
- No JavaScript errors in browser console (F12 → Console)

### ❌ Potential Issues
- **Model dropdowns stay disabled**: Provider selection not working
- **"No models available"**: modelData not loading correctly  
- **Form doesn't submit**: Missing required fields
- **Download doesn't work**: Browser blocking downloads

## Browser Console Testing

Open browser developer tools (F12) and check the Console tab:

### Expected (No Errors)
```
No error messages
```

### If You See Errors
```javascript
// Common issues:
"Cannot read property 'value' of null" → Element ID mismatch
"modelData is not defined" → Script loading issue  
"Cannot read property 'style' of null" → DOM element missing
```

## Testing Different Browsers

Try in multiple browsers:
- ✅ **Chrome**: Should work perfectly
- ✅ **Firefox**: Should work perfectly  
- ✅ **Safari**: Should work perfectly
- ✅ **Edge**: Should work perfectly
- ⚠️ **Older browsers**: May have issues with modern JavaScript

## Mobile Testing

Test on phone/tablet:
- Interface should be responsive
- Dropdowns should work with touch
- Form should submit correctly
- Download may save to device downloads folder

## Troubleshooting Steps

### Issue: Model dropdowns don't populate
1. **Check browser console** for JavaScript errors
2. **Try different provider** (Claude, Gemini, OpenAI)
3. **Refresh page** and try again
4. **Try different browser** (Chrome recommended)

### Issue: Can't download Python script
1. **Check browser download settings** - allow downloads
2. **Try right-click → Save As** on download button
3. **Check Downloads folder** - file may be there
4. **Try different browser** - some block downloads

### Issue: OpenRouter mode not working
1. **Check that text inputs appear** when selecting OpenRouter
2. **Verify Direct API fields disappear** when switching modes
3. **Enter valid model names** like `anthropic/claude-3.5-sonnet`

## Report Issues

If you find problems:
1. **Note your browser** and version
2. **Check console errors** (F12 → Console)
3. **Describe exact steps** that don't work
4. **Try on different browser** to confirm

The interface should work smoothly with immediate model loading when you select providers!