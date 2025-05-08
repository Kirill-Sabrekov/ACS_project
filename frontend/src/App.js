import React, { useState, useEffect, useCallback, memo, useMemo } from "react";
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js';
import "./App.css";

// Регистрируем компоненты Chart.js
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

const ChartBlock = memo(function ChartBlock({ history, tagname, formatValue }) {
  const sortedHistory = useMemo(() => {
    if (!history || !Array.isArray(history)) return [];
    return [...history].sort((a, b) => new Date(a.time) - new Date(b.time));
  }, [history]);

  const labels = useMemo(() => 
    sortedHistory.map(item => {
      try {
        return new Date(item.time).toLocaleString('ru-RU', {
          year: 'numeric',
          month: '2-digit',
          day: '2-digit',
          hour: '2-digit',
          minute: '2-digit',
          second: '2-digit'
        });
      } catch (e) {
        console.error('Ошибка форматирования даты:', e);
        return item.time;
      }
    }), 
    [sortedHistory]
  );

  const values = useMemo(() => 
    sortedHistory.map(item => {
      try {
        return formatValue(item);
      } catch (e) {
        console.error('Ошибка форматирования значения:', e);
        return null;
      }
    }), 
    [sortedHistory, formatValue]
  );

  const data = useMemo(() => ({
    labels,
    datasets: [
      {
        label: tagname,
        data: values,
        borderColor: '#4CAF50',
        backgroundColor: 'rgba(76,175,80,0.1)',
        tension: 0.4,
        pointRadius: 4,
        pointHoverRadius: 7,
        pointBackgroundColor: '#fff',
        pointBorderColor: '#4CAF50',
        pointBorderWidth: 2,
        fill: true
      }
    ]
  }), [labels, values, tagname]);

  const options = useMemo(() => ({
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { position: 'top', labels: { color: '#b2ffb2' } },
      title: { display: true, text: 'История измерений', color: '#b2ffb2', font: { size: 18 } },
      tooltip: {
        backgroundColor: '#232837',
        titleColor: '#4CAF50',
        bodyColor: '#f3f3f3',
        borderColor: '#4CAF50',
        borderWidth: 1
      }
    },
    scales: {
      x: {
        ticks: { color: '#b2ffb2' },
        grid: { color: 'rgba(76,175,80,0.08)' }
      },
      y: {
        beginAtZero: true,
        ticks: { color: '#b2ffb2' },
        grid: { color: 'rgba(76,175,80,0.08)' }
      }
    }
  }), []);

  if (!history || history.length === 0) {
    return <div className="no-data">Нет данных для отображения</div>;
  }

  return (
    <div className="chart-container">
      <Line data={data} options={options} />
    </div>
  );
});

function App() {
  const [tagnames, setTagnames] = useState([]);
  const [selectedNodeId, setSelectedNodeId] = useState("");
  const [sensorData, setSensorData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [dateFrom, setDateFrom] = useState("");
  const [dateTo, setDateTo] = useState("");

  const fetchTagnames = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await fetch("http://localhost:8000/api/v1/tagnames");
      if (!response.ok) {
        throw new Error(`Ошибка при загрузке списка датчиков: ${response.status}`);
      }
      const data = await response.json();
      if (Array.isArray(data)) {
        setTagnames(data);
      } else {
        console.error("Полученные данные не являются массивом:", data);
        setTagnames([]);
      }
    } catch (err) {
      setError(`Ошибка при загрузке списка датчиков: ${err.message}`);
      console.error(err);
      setTagnames([]);
    } finally {
      setLoading(false);
    }
  }, []);

  const fetchSensorData = useCallback(async () => {
    if (!selectedNodeId) {
      setSensorData([]);
      return;
    }
    
    try {
      setLoading(true);
      setError(null);
      let url = `http://localhost:8000/api/v1/data?nodeid=${selectedNodeId}`;
      if (dateFrom) url += `&date_from=${encodeURIComponent(dateFrom)}`;
      if (dateTo) url += `&date_to=${encodeURIComponent(dateTo)}`;
      
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error(`Ошибка при загрузке данных датчика: ${response.status}`);
      }
      
      const data = await response.json();
      if (Array.isArray(data) && data.length > 0) {
        setSensorData(data);
      } else {
        setSensorData([]);
        setError("Нет данных для выбранного периода");
      }
    } catch (err) {
      setError(`Ошибка при загрузке данных датчика: ${err.message}`);
      console.error(err);
      setSensorData([]);
    } finally {
      setLoading(false);
    }
  }, [selectedNodeId, dateFrom, dateTo]);

  useEffect(() => {
    fetchTagnames();
  }, [fetchTagnames]);

  useEffect(() => {
    if (selectedNodeId) {
      fetchSensorData();
    }
  }, [selectedNodeId, fetchSensorData]);

  const formatValue = useCallback((item) => {
    if (item === null || item === undefined) return "Нет данных";
    
    if (item.valdouble !== null && item.valdouble !== undefined) return item.valdouble;
    if (item.valint !== null && item.valint !== undefined) return item.valint;
    if (item.valuint !== null && item.valuint !== undefined) return item.valuint;
    if (item.valbool !== null && item.valbool !== undefined) return item.valbool ? "Да" : "Нет";
    if (item.valstring !== null && item.valstring !== undefined) return item.valstring;
    
    return "Нет данных";
  }, []);

  const formatDate = useCallback((dateString) => {
    try {
      return new Date(dateString).toLocaleString('ru-RU', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
      });
    } catch (e) {
      console.error('Ошибка форматирования даты:', e);
      return dateString;
    }
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>Мониторинг датчиков</h1>
      </header>
      <main>
        <div className="controls">
          <select
            value={selectedNodeId}
            onChange={(e) => setSelectedNodeId(e.target.value)}
            disabled={loading}
          >
            <option value="">-- Выберите датчик --</option>
            {tagnames.map((tag) => (
              <option key={tag.nodeid} value={tag.nodeid}>
                {tag.tagname}
              </option>
            ))}
          </select>
          <input
            type="datetime-local"
            value={dateFrom}
            onChange={e => setDateFrom(e.target.value)}
            style={{marginLeft: 10}}
            placeholder="От"
            disabled={loading}
          />
          <input
            type="datetime-local"
            value={dateTo}
            onChange={e => setDateTo(e.target.value)}
            style={{marginLeft: 10}}
            placeholder="До"
            disabled={loading}
          />
          <button 
            onClick={fetchSensorData} 
            style={{marginLeft: 10}}
            disabled={loading || !selectedNodeId}
          >
            {loading ? 'Загрузка...' : 'Обновить данные'}
          </button>
        </div>

        {error && <div className="error">{error}</div>}

        {loading ? (
          <div className="loading">Загрузка...</div>
        ) : sensorData.length > 0 ? (
          <div className="sensor-data">
            <h2>{sensorData[0].tagname}</h2>
            <ChartBlock
              history={sensorData[0].history}
              tagname={sensorData[0].tagname}
              formatValue={formatValue}
            />
            <table>
              <thead>
                <tr>
                  <th>Время</th>
                  <th>Значение</th>
                  <th>Качество</th>
                </tr>
              </thead>
              <tbody>
                {sensorData[0].history.map((item, index) => (
                  <tr key={index}>
                    <td>{formatDate(item.time)}</td>
                    <td>{formatValue(item)}</td>
                    <td>{item.quality || ""}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : selectedNodeId && !loading && !error ? (
          <div className="no-data">Нет данных для отображения</div>
        ) : null}
      </main>
    </div>
  );
}

export default App;
