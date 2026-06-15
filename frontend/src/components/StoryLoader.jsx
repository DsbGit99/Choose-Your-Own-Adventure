import {useEffect, useState} from 'react';
import {useParams, useNavigate} from 'react-router-dom'
import axios from 'axios';
import LoadingStatus from "./LoadingStatus";
import StoryGame from './StoryGame';
import {API_BASE_URL} from "../util";

function StoryLoader() {
    // --------------------------------- hooks ----------------------------------

    const {id} = useParams();   // gets dynamic id element
    const navigate = useNavigate();  // navigation object

    const [story, setStory] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    // TODO: Test if this useEffect is actually needed.
    // This is the browser ID. Will a change in it change state?
    useEffect(() => loadStory(id), [id])

    // ----------------------- functions & event handlers -----------------------

    const loadStory = async (storyId) => {
        setLoading(true);
        setError(null);

        try{
            // calls the get_complete_story router using a story_id
            const response = await axios.get(
                `${API_BASE_URL}/stories/${storyId}/complete`
            )
            setStory(response)
        } catch (e) {
            if (e.response?.status === 404) {
                setError("Story is not found")
            }
            else {
                setError("Failed to load story")
            }
        } finally {
            setLoading(false)
        }
    }

    const createNewStory = () => {
        navigate('/')
    }

    // ---------------------------- return component ----------------------------

    if (loading) {
        {/*TODO: Make this return the actual theme. */}
        return <LoadingStatus theme={"story"}/>
    }

    if (error) {
        return <div className="error-message">
            <h2>Story Not Found</h2>
            <p>{error}</p>
            <button onClick={createNewStory}>Go to Story Generator</button>
        </div>
    }

    if (story) {
        return <div className='story-loader'>
            <StoryGame story={story} onNewStory={createNewStory} />
        </div>
    }
}

export default StoryLoader;
