import React, { useEffect, useState } from 'react';
import './ScrapedData.css';
import { useNavigate } from 'react-router-dom';
import { FaBackward, FaDashcube, FaHome } from 'react-icons/fa';

const ITEMS_PER_PAGE = 15;

const ScrapedData = () => {
  const [data, setData] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [minPrice, setMinPrice] = useState('');
  const [maxPrice, setMaxPrice] = useState('');

  const navigate = useNavigate();
  const fetchData = () => {
    fetch('http://localhost:5000/api/scraped-data')
      .then(res => res.json())
      .then(json => {
        setData(json);
        setCurrentPage(1);
      })
      .catch(err => {
        console.error('Error fetching default data:', err);
        setData([]);
      });
  };

  // ✅ The new searchResults handler to hit the filtered endpoint
  const searchResults = (min, max) => {
    let url = 'http://localhost:5000/api/scraped-data/search';
    const params = new URLSearchParams();

    if (min) params.append('min_price', min);
    if (max) params.append('max_price', max);

    fetch(`${url}?${params.toString()}`)
      .then(res => res.json())
      .then(json => {
        if (Array.isArray(json)) {
          setData(json);
          setCurrentPage(1);
        } else {
          setData([]);
        }
      })
      .catch(err => {
        console.error('Error fetching filtered data:', err);
        setData([]);
      });
  };

  // ✅ Trigger default fetch when component mounts
  useEffect(() => {
    fetchData();
  }, []);

  const handleSearch = () => {
    searchResults(minPrice, maxPrice);
  };

  const isArray = Array.isArray(data);
  const totalPages = isArray ? Math.ceil(data.length / ITEMS_PER_PAGE) : 0;
  const paginatedData = isArray
    ? data.slice((currentPage - 1) * ITEMS_PER_PAGE, currentPage * ITEMS_PER_PAGE)
    : [];

  const handlePrev = () => {
    if (currentPage > 1) setCurrentPage(prev => prev - 1);
  };

  const handleNext = () => {
    if (currentPage < totalPages) setCurrentPage(prev => prev + 1);
  };

  return (
    <div className="scraped-data-screen">
        <button className="back-button" onClick={() => navigate('/dashboard')}>
          <FaHome /> Home
        </button>
      <h2>📦 Scraped Listings</h2>
      {/* Price Filter */}
      <div className="filter-controls">
        <input
          type="number"
          placeholder="Min Price"
          value={minPrice}
          onChange={e => setMinPrice(e.target.value)}
        />
        <input
          type="number"
          placeholder="Max Price"
          value={maxPrice}
          onChange={e => setMaxPrice(e.target.value)}
        />
        <button onClick={handleSearch}>Search Results in This Range.</button>
      </div>

      {/* Table */}
      <div className="scraped-table-container">
        <table className="scraped-table">
          <thead>
            <tr>
              <th>Record#</th>
              <th>Scraped Date</th>
              <th>Price</th>
              <th>Status</th>
              <th>Detail URL</th>
              <th>City</th>
              <th>State</th>
              <th>Zip Code</th>
              <th>Bedrooms avail</th>
              <th>Bathsrooms avail</th>
              <th>Broker name</th>
            </tr>
          </thead>
          <tbody>
            {paginatedData.length > 0 ? (
              paginatedData.map((item, index) => (
                <tr key={index}>
                  <td>{(currentPage - 1) * ITEMS_PER_PAGE + index + 1}</td>
                  <td>{item.scraped_date}</td>
                  <td>{item.property_price?.toLocaleString()}</td>
                  <td>{item.status_type}</td>
                  <td><a href={item.property_detail_url} target="_blank" rel="noopener noreferrer">View</a></td>
                  <td>{item.property_city}</td>
                  <td>{item.property_state}</td>
                  <td>{item.property_address_zip_code}</td>
                  <td>{item.bedrooms_available}</td>
                  <td>{item.bathrooms_available}</td>
                  <td>{item.broker_name}</td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan="11">Loading or no data available...</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      {/* Pagination Controls */}
      {isArray && data.length > ITEMS_PER_PAGE && (
        <div className="pagination-controls">
          <button onClick={handlePrev} disabled={currentPage === 1}>← Prev</button>
          <span>Page {currentPage} of {totalPages}</span>
          <button onClick={handleNext} disabled={currentPage === totalPages}>Next →</button>
        </div>
      )}
    </div>
  );
};

export default ScrapedData;
