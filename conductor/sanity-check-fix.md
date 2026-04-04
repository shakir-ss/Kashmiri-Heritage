# Implementation Plan: Deployment Sanity Check & API Path Fix

The platform is experiencing issues on Vercel because several views were using relative API paths (e.g., `/api/orders/admin`) instead of using the configured `API_URL`. This caused those calls to hit the Vercel frontend instead of the Render backend. Additionally, trailing slashes in `VITE_API_URL` could cause double-slashes in some calls.

## Objective
Standardize API pathing using `axios.defaults.baseURL` and fix environment-specific URL inconsistencies.

## Key Files & Context
- `frontend/src/config.js`: Strips trailing slash from `API_URL`.
- `frontend/src/main.js`: Configures `axios.defaults.baseURL`.
- `frontend/src/stores/*`: Cleaned up to remove redundant `${API_URL}` prefixes.
- `frontend/src/views/*`: Fixed to ensure they use the `axios` instance configured with the `baseURL`.

## Implementation Steps

### 1. Standardize API URL Configuration
- [x] Modify `frontend/src/config.js` to strip any trailing slash from `import.meta.env.VITE_API_URL`.
- [x] Update `frontend/src/main.js` to set `axios.defaults.baseURL = API_URL`.

### 2. Batch Store Cleanup
- [x] Remove explicit `${API_URL}` prefixes from all store files (`authStore.js`, `productStore.js`, `analyticsStore.js`, `cartStore.js`, `wishlistStore.js`).
- [x] This ensures that all store calls now use the `baseURL` set in `main.js`.

### 3. Verify Product Loading
- If products still don't load after these fixes, the likely cause is an empty production database.
- Action: Advise the user to run the themed data seeding script on their Render/TiDB environment.

## Verification & Testing
1. **Local Test**: Run `npm run dev` and ensure login and product fetching still work correctly with the new `baseURL` configuration.
2. **Vercel Test**: Ensure `VITE_API_URL` is set in Vercel environment variables (e.g., `https://kashmiri-heritage-backend.onrender.com`).
3. **Admin Check**: Log in as `root@thehundredvillages.com` and verify the Admin Dashboard stats and inventory load correctly.
