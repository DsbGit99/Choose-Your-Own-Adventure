import { useState } from "react";

function ThemeInput({onSubmit}) {
    // --------------------------------- hooks ----------------------------------

    const [theme, setTheme] = useState("");
    const [error, setError] = useState("");

    // ----------------------- functions & event handlers -----------------------

    /* Note how we do not need to curry here. Furthermore, note how when we
    actually decalre handleSubmit within the onSubmit prop (in the form element):
    
    onSubmit={handleSubmit}

    ...there are no passed arguments.

    This is because in react, e (event) is the singular default parameter
    provided to event handlers.

    We also would have been able to likewise avoid currying if one of the state
    variables declared above were passed.
    
    If this handler were a one-liner, it would have looked similar to
    this (in the form's input element).

    onChange={(e) => setTheme(e.target.value)}

    If we wanted to use the default e (event) parameter AND our own parameters,
    then we could do somthing like this (not done here):

    const handleChange = (fieldName) => (event) => { <...> }

    ...then passing parameters:

    onChange={handleChange("<field>")}

    ...where e (event) is implicitly passed and "<field>" is explicitly passed.
W
    */

    const handleSubmit = (e) => {
        e.preventDefault(); // Prevents page reload

        if (!theme.trim()) {
            setError("Please enter a theme name");
            return
        }

        /* This is a callback function's prop.
        The parent component state gets lifted to is StoryGenerator.
        The event being handled, meanwhile, is the form found returned here. */
        onSubmit(theme);
    }

    // ---------------------------- return component ----------------------------

    return <div className="theme-input-container">
        <h2>Generate Your Adventure</h2>
        <p>Enter a theme for your interactive story</p>

        <form onSubmit={handleSubmit}>
            <div className="input-group">
                <input 
                    type="text"
                    value={theme}
                    onChange={(e) => setTheme(e.target.value)}
                    placeholder="Enter a theme (e.g. prirates, space, medieval...)"
                    className={error ? 'error' : ''}    // highlight box if error
                />

                {/* ...also provides some error text if applicable. */} 
                {error && <p className="error-text">{error}</p>}
            </div>
            <button type="submit" className="generate-btn">
                Generate Story
            </button>
        </form>
    </div>
}

export default ThemeInput;
