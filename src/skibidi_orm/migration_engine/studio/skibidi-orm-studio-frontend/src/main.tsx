import { RouterProvider, createRouter } from '@tanstack/react-router'
import "ag-grid-community/styles/ag-grid.css"; // Mandatory CSS required by the grid
import "ag-grid-community/styles/ag-theme-quartz.css"; // Optional Theme applied to the grid
import React from 'react'
import ReactDOM from 'react-dom/client'
import { Providers } from './components/Providers.tsx'
import './index.css'
import { routeTree } from './routeTree.gen'
import './styles/ag-custom.css'

const router = createRouter({ routeTree })
declare module '@tanstack/react-router' {
  interface Register {
    router: typeof router
  }
}

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <Providers>
      <RouterProvider router={router} />
    </Providers>
  </React.StrictMode>,
)
