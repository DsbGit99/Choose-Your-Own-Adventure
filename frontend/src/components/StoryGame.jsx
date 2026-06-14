import {useState, useEffect} from 'react';

function StoryGame ({story, onNewStory}) {
    // --------------------------------- hooks ----------------------------------

    const [currentNodeID, setCurrentNodeID] = useSate(null);
    const [currentNode, setCurrentNode] = useSate(null);
    const [options, setOptions] = useState([]);
    const [isEnding, setIsEnding] = useState(false);
    const [isWinningEnding, setIsWinningEnding] = useState(false);

    // TODO: Does story already change state? Can we remove these useEffects?
    useEffect(() => {
        if (story?.root_node) {
            // TODO: Do we need to pass by value?
            // Is this becuase rootNodeId isn't primitive?
            const rootNodeId = story.rootNodeId
            setCurrentNodeID(rootNodeId)
        }
    }, [story])

    useEffect(() => {
        if (currentNodeID && story?.all_nodes) {
            // get node from ID
            const node = story.all_nodes[currentNodeID]
            
            // use to set current node
            setCurrentNode(node)
            setIsEnding(node.isEnding)
            setIsWinningEnding(node.isWinningEnding)

            if (!node.isWinningEnding && node.options && node.options.length > 0) {
                setOptions(node.options)
            } else {
                setOptions([])
            }
        }
    }, [currentNodeID, story])

    // ----------------------- functions & event handlers -----------------------

     
    /* NOTE: We could have also just passed this into onClick as:

    onClick={(optionId) => setCurrentNodeID(optionId)}

    We chose to instead curry this into a function with name chooseOption,
    as the name better reinforces what is going done at a higher-level.

    We are abstracting the idea of setting the current node ID to choosing a 
    story option.

    onClick={(optionId) => chooseOption(optionId)}

    Again, note the currying! */

    const chooseOption = (optionId) => () => {
        setCurrentNodeID(optionId)  
    }
    
    const restartStory = () => {
        if (story?.root_node) {
            setCurrentNodeID(story.root_node.id)
        }
    }

    // ---------------------------- return component ----------------------------

    return <div className="story-game">
        <header className="story-header">
            <h2>{story.title}</h2>
        </header>

        <div className="story-content">
            {/* Display story content for current node. */}
            <p>{currentNode.content}</p>

            {isEnding ?
                // Story has ended.
                <div className="story-ending">
                    <h3>{isWinningEnding ? "Congratulations" : "The End"}</h3>
                    {isWinningEnding ?
                        "You reached a winning ending" : "Your adventure has ended."
                    }
                </div>
                :
                // Story is continuing. Show options.
                <div className="story-options">
                    <h3>What will you do?</h3>
                    <div className="options-list">
                        {options.map((options, index) => {
                            return <button>
                                key={index}
                                onClick={chooseOption(options.node_id)}
                                className="option-btn"
                            </button>
                            {options.text}
                        })}
                    </div>
                </div>
            }
        </div>

        <div className="story-controls">
            <button onClick={restartStory} className="reset-btn">
                Restart Story
            </button>
        </div>
        
        {/*
            Only show this button if we have a new story.
            It will navigate us to where we can create a new story.
            
            TODO: ...but do we actually need the && here?
        */}
        {onNewStory && <button onClick={onNewStory} className="new-story-btn">
            New Story
        </button>}
    </div>
}

export default StoryGame;
