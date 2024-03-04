import { Button } from "react-bootstrap";

export function ClearButton(){
    const clearInput = () => {
        // Sets the "filteredData" state to an empty array, effectively clearing any previously filtered data
        setFilteredData([]);

        // Sets the "wordEntered" state to an empty string, resetting the search word
        setWordEntered("");
    }

    return(
        <>
            <Button onClick={clearInput}>Clear</Button>
        </>
    );
}