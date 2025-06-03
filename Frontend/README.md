# Frontend

The `Frontend` directory contains the user interface and client-side logic for the VisionXAI project. This Angular application is managed with Nx and is designed for a responsive, modern user experience.

## Key Features

- **Responsive Design**: Built with a mobile-first approach using Angular and Tailwind CSS for seamless experiences across devices.
- **Dynamic User Interface**: Uses Angular components and modules for a dynamic, interactive UI.
- **Server-Side Rendering (SSR)**: SSR is supported via Angular Universal for improved performance and SEO. See `main.server.ts` and `server.ts` for implementation.
- **Theming and Customization**: Customizable themes are managed in `mytheme.ts`.
- **State Management**: Utilizes Angular's built-in services for state management. (No third-party state library is used by default.)
- **API Integration**: Integrates with backend services using Angular's HTTP client for RESTful API communication.
- **Testing and Quality Assurance**: Configured with Jest for unit and integration tests. See `jest.config.ts` and `test-setup.ts`.

## Setup Instructions

1. **Install Dependencies**: Run `npm install --legacy-peer-deps` in this directory to install all dependencies.
2. **Configuration**: Ensure configuration files like `tsconfig.json` and `tailwind.config.js` are set up for your environment. Adjust `vercel.json` for deployment if needed.

## Running the Application

- **Development Server**: Start the dev server with:

  ```sh
  npx nx serve Frontend
  ```

  This enables hot-reloading for rapid development.

- **Production Build**: Create a production build with:
  ```sh
  npx nx build Frontend
  ```
  The output will be optimized for deployment.

## Testing

Run all tests with:

```sh
npx nx test Frontend
```

Jest is configured to provide detailed reports and coverage analysis.

## Build and Deployment

- The build process is managed by Nx for efficient compilation and bundling.
- Deployment can be configured in `vercel.json` or other deployment-specific files for platforms like Vercel.

## Project Structure

- `src/` — Main source code (Angular app, entry points, styles, theme)
- `public/` — Static assets
- `app/` — Angular components, services, routes, and shared modules

## Additional Resources

- [Nx Documentation](https://nx.dev)
- [Angular Documentation](https://angular.io/docs)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
