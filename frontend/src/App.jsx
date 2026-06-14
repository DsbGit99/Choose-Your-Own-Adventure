import './App.css'
import {Routes, Route} from "react-router-dom"
import StoryLoader from "./components/StoryLoader"
import StoryGenerator from "./components/StoryGenerator.jsx";

function App() {
  // ---------------------------- return component ----------------------------

  return (
    <div className="app-container">
      <header>
        <h1>Interactive Story Generator</h1>
      </header>
      <main>
        <Routes>
          <Route path={"/story/:id"} element={<StoryLoader />} />
          <Route path={"/"} element={<StoryGenerator />}/>
        </Routes>
      </main>
    </div>
  )
}

export default App