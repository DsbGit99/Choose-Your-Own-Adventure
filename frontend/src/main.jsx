import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import {BrowserRouter as Router} from "react-router-dom"
import './index.css'
import App from './App.jsx'

/* TODO: In React 19, BrowserRouter may no longer be reccomended in favor of
another method... However! For now, it seems to work. */

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <Router>
      <App />
    </Router>
  </StrictMode>,
)
