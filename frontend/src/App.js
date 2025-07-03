import React, { useState, useEffect } from 'react';
import axios from 'axios';

function App() {
  const [users, setUsers] = useState([]);
  const [form, setForm] = useState({ first_name: '', last_name: '', email: '', phone: '', pan: '' });
  const [showPan, setShowPan] = useState(false);
  const [editingId, setEditingId] = useState(null);

  const fetchUsers = async () => {
    const res = await axios.get('http://localhost:8000/users');
    setUsers(res.data);
  };

  useEffect(() => { fetchUsers(); }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const url = editingId ? `http://localhost:8000/edit/${editingId}` : 'http://localhost:8000/create';
    await axios[editingId ? 'put' : 'post'](url, form);
    setForm({ first_name: '', last_name: '', email: '', phone: '', pan: '' });
    setEditingId(null);
    fetchUsers();
  };

  const handleEdit = (user) => {
    setForm(user);
    setEditingId(user.id);
  };

  const handleDelete = async (id) => {
    if (window.confirm("Delete user?")) {
      await axios.delete(`http://localhost:8000/delete/${id}`);
      fetchUsers();
    }
  };

  const handleUpload = async (e) => {
    const formData = new FormData();
    formData.append('file', e.target.files[0]);
    try {
      await axios.post('http://localhost:8000/upload', formData);
      fetchUsers();
    } catch (err) {
      alert(JSON.stringify(err.response.data.detail));
    }
  };

  return (
    <div>
      <h2>User Form</h2>
      <form onSubmit={handleSubmit}>
        {['first_name', 'last_name', 'email', 'phone', 'pan'].map(field => (
          <div key={field}>
            <input type={field === 'pan' && !showPan ? 'password' : 'text'}
              placeholder={field} value={form[field] || ''}
              onChange={e => setForm({ ...form, [field]: e.target.value })} />
            {field === 'pan' && <button type="button" onClick={() => setShowPan(!showPan)}>👁️</button>}
          </div>
        ))}
        <button type="submit">{editingId ? 'Update' : 'Create'}</button>
      </form>

      <h2>Upload Excel</h2>
      <input type="file" onChange={handleUpload} />

      <h2>User List</h2>
      <table border="1">
        <thead>
          <tr><th>ID</th><th>First</th><th>Last</th><th>Email</th><th>Phone</th><th>PAN</th><th>Actions</th></tr>
        </thead>
        <tbody>
          {users.map(u => (
            <tr key={u.id}>
              <td>{u.id}</td><td>{u.first_name}</td><td>{u.last_name}</td><td>{u.email}</td>
              <td>{u.phone}</td><td>{showPan ? u.pan : '••••••••••'}</td>
              <td>
                <button onClick={() => handleEdit(u)}>Edit</button>
                <button onClick={() => handleDelete(u.id)}>Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default App;
