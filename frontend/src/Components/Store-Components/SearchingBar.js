import React from "react";

export function SearchingBar({ query, setQuery }) {
  const handleChange = (event) => {
    setQuery(event.target.value);
  }

  return (
    <>
      <input
        type="text"
        value={query}
        onChange={handleChange}
        placeholder="Search..."
      />
    </>
  );
}
