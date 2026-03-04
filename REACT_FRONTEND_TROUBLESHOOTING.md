# React Frontend Troubleshooting Guide

## Issue: White Screen After "Optimizing Dependencies"

### Symptoms
- Dev server starts successfully
- Shows "optimizing dependencies" message
- Page loads but shows white screen
- No visible error messages

### Root Cause
This is typically caused by:
1. Runtime JavaScript errors
2. Missing dependencies
3. Import path issues
4. Component rendering errors

### Solution Steps

#### Step 1: Clear Cache and Restart

```bash
cd frontend-react

# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install

# Clear Vite cache
rm -rf node_modules/.vite

# Restart dev server
npm run dev
```

#### Step 2: Check Browser Console

1. Open the application in browser
2. Open Developer Tools (F12 or Cmd+Option+I)
3. Go to Console tab
4. Look for error messages (red text)
5. Note the error message and stack trace

#### Step 3: Check Terminal Output

Look for error messages in the terminal where `npm run dev` is running.

Common errors:
- `Cannot find module` - Missing dependency
- `Unexpected token` - Syntax error
- `X is not defined` - Import issue

#### Step 4: Error Boundary

The app now includes an ErrorBoundary component that will catch and display runtime errors with full stack traces.

If you see the error boundary screen:
1. Read the error message
2. Check the stack trace
3. Note which component is failing

### Common Issues and Fixes

#### Issue 1: Port Already in Use

**Error:** `Port 3000 is in use, trying another one...`

**Solution:**
```bash
# Find process using the port
lsof -i :3000

# Kill the process
kill -9 <PID>

# Or use a different port
npm run dev -- --port 3005
```

#### Issue 2: Module Not Found

**Error:** `Cannot find module '@/components/...'`

**Solution:**
```bash
# Check if file exists
ls -la frontend-react/src/components/

# Reinstall dependencies
npm install
```

#### Issue 3: TypeScript Errors

**Error:** Type errors in console

**Solution:**
```bash
# Check for TypeScript errors
npx tsc --noEmit

# If errors found, fix them in the source files
```

#### Issue 4: Tailwind CSS Not Working

**Error:** Styles not applying

**Solution:**
```bash
# Verify Tailwind is installed
npm list tailwindcss

# Check tailwind.config.js exists
cat tailwind.config.js

# Restart dev server
npm run dev
```

### Debug Mode

To run with more verbose output:

```bash
# Enable debug mode
DEBUG=vite:* npm run dev

# Or with Node.js debugging
NODE_OPTIONS='--inspect' npm run dev
```

### Build Test

Test if the app builds successfully:

```bash
# Try building for production
npm run build

# If build succeeds, the issue is dev-server specific
# If build fails, there are code errors to fix
```

### Network Issues

If the page loads but API calls fail:

1. **Check Backend is Running**
   ```bash
   curl http://localhost:8000/health
   ```

2. **Check CORS Configuration**
   - Backend should allow `http://localhost:3001`
   - Check `backend/api/main.py` CORS settings

3. **Check API Proxy**
   - Verify `vite.config.ts` proxy configuration
   - Should proxy `/api` to `http://localhost:8000`

### Complete Reset

If all else fails, complete reset:

```bash
cd frontend-react

# Remove everything
rm -rf node_modules package-lock.json dist .vite

# Reinstall
npm install

# Restart
npm run dev
```

### Getting Help

If the issue persists:

1. **Collect Information:**
   - Error message from browser console
   - Error message from terminal
   - Node.js version: `node --version`
   - npm version: `npm --version`
   - Operating system

2. **Check Documentation:**
   - `REACT_FRONTEND_SETUP_COMPLETE.md`
   - `REACT_FRONTEND_PHASE2_COMPLETE.md`
   - `REACT_FRONTEND_ERROR_CHECK.md`

3. **Common Solutions:**
   - Update Node.js to v18.20.8 or higher
   - Clear browser cache
   - Try incognito/private browsing mode
   - Disable browser extensions

### Prevention

To avoid issues in the future:

1. **Always use correct Node.js version**
   ```bash
   node --version  # Should be v18+
   ```

2. **Keep dependencies updated**
   ```bash
   npm outdated
   npm update
   ```

3. **Use consistent package manager**
   - Stick to npm (don't mix with yarn/pnpm)

4. **Commit package-lock.json**
   - Ensures consistent installs

### Quick Reference

```bash
# Start dev server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Check for errors
npx tsc --noEmit

# Clear cache
rm -rf node_modules/.vite

# Full reinstall
rm -rf node_modules package-lock.json && npm install
```

---

## Current Status

✅ **ErrorBoundary Added** - Will catch and display runtime errors  
✅ **TypeScript Configured** - Type checking enabled  
✅ **Vite Optimized** - Fast HMR and builds  
✅ **Tailwind CSS** - Styling framework ready  

**Next Steps:**
1. Restart dev server: `npm run dev`
2. Open browser: http://localhost:3001/
3. Check console for any errors
4. If white screen persists, ErrorBoundary will show the error

---

*Last Updated: March 4, 2024*