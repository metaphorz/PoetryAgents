#!/usr/bin/env zsh

# Quick fix for dropdown issue
echo "🔧 Applying quick dropdown fix..."

# Check if the issue is in the function call parameters
echo "Checking function call syntax..."

if grep -q "loadModelsForPoet(1, this.value)" poetry_generator_live.html; then
    echo "✅ Function calls look correct"
else
    echo "⚠️  Function call syntax may be incorrect"
fi

# Check if DOMContentLoaded is properly set up
if grep -q "DOMContentLoaded.*function" poetry_generator_live.html; then
    echo "✅ DOMContentLoaded listener found"
else
    echo "❌ DOMContentLoaded listener missing"
fi

echo ""
echo "💡 Next steps:"
echo "1. Open live_test_dropdown.html in browser"
echo "2. Check browser console for errors"
echo "3. Try the manual test buttons"
echo "4. Look at the data inspection results"
