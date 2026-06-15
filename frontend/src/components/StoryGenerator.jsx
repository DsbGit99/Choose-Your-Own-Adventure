import {useState, useEffect} from "react"
import {useNavigate} from "react-router-dom";
import axios from "axios";
import ThemeInput from "./ThemeInput";
import LoadingStatus from "./LoadingStatus";
import {API_BASE_URL} from "../util";

// NOTE: This is the component shown at the root path.

function StoryGenerator() {

    // --------------------------------- hooks ----------------------------------

    const navigate = useNavigate()
    const [theme, setTheme] = useState("")
    const [jobId, setJobId] = useState(null)
    const [jobStatus, setJobStatus] = useState(null)
    const [error, setError] = useState(null)
    const [loading, setLoading] = useState(false)

    // TODO: Consdier if we really need this useEffect.
    useEffect(() => {
        let pollInterval;

        if (jobId && jobStatus === "processing") {
            pollInterval = setInterval(() => {
                pollJobStatus(jobId)
            }, 5000)
        }

        return () => {
            if (pollInterval) {
                clearInterval(pollInterval)
            }
        }
    }, [jobId, jobStatus])

    // ----------------------- functions & event handlers -----------------------

    /* Notice that we do NOT curry here. This is because theme is declared above
    as a state variable. */

    const generateStory = async (theme) => {
        setLoading(true)
        setError(null)
        setTheme(theme)

        try {
            // POST, then set job ID and status
            const response = await axios.post(`${API_BASE_URL}/stories/create`, {theme})
            const {job_id, status} = response.data
            setJobId(job_id)
            setJobStatus(status)    // not redundant, since getter *could* fail.

            // poll job status via its ID
            pollJobStatus(job_id)

        } catch (e) {
            setLoading(false)
            setError(`Failed to generate story: ${e.message}`)
        }
    }

    const pollJobStatus = async (id) => {

        try {
            // GET job status via id (from api), then use job status setter.
            const response = await axios.get(`${API_BASE_URL}/jobs/${id}`)
            const {status, story_id, error: jobError} = response.data

            /* NOTE: This setJobStatus call does NOT cause an infinite loop with
            useEffect. "processing" may not change upon calling GET... or it may!
            but will only change once, either to "completed" or "failed".*/
            setJobStatus(status)
            
            if (status === "completed" && story_id) {
                // fetch story if its job has "completed".
                setLoading(false)
                fetchStory(story_id)
            } else if (status === "failed" || jobError) {
                // otherwise, if the status is "failed" set job error.
                setLoading(false)
                setError(jobError || "Failed to generate story")
            }

            // if still "processing", we will poll again soon.

        } catch (e) {
            // (note: not to be confused with job error)
            setLoading(false)
            setError(`Failed to check story status: ${e.message}`)
        }
    }

    const fetchStory = () => {
        try {
            navigate(`/story/${id}`)
        } catch (e) {
            setError(`Failed to load story: ${e.message}`)
        }
    }

    const reset = () => {
        setTheme("")
        setJobId(null)
        setJobStatus(null)
        setError(null)
        setLoading(false)
    }

    // ---------------------------- return component ----------------------------

    return <div className="story-generator">
        {/* Error */}
        {error && <div className="error-message">
            <p>{error}</p>
            <button onClick={reset}>Try Again</button>
        </div>}
        
        {/* Display ThemeInput, then generate story. */}
        {!jobId && !error && !loading && <ThemeInput onSubmit={generateStory}/>}
        
        {/* Loading (TODO: Can we use Suspense here?) */}
        {loading && <LoadingStatus theme={theme} />}
    </div>
}


export default StoryGenerator