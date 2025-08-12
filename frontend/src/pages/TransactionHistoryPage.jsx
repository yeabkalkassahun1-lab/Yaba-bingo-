// src/pages/TransactionHistoryPage.jsx
import React, { useState, useEffect } from 'react';
import useAxios from '../hooks/useAxios';

function TransactionHistoryPage() {
    const [transactions, setTransactions] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const api = useAxios();

    useEffect(() => {
        const fetchTransactions = async () => {
            try {
                const response = await api.get('/api/transactions/');
                setTransactions(response.data);
            } catch (err) {
                setError('Failed to load transaction history.');
            } finally {
                setLoading(false);
            }
        };
        fetchTransactions();
    }, []);

    const formatCurrency = (value) => {
        return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'ETB' }).format(value);
    };

    if (loading) return <p>Loading history...</p>;
    if (error) return <p className="error-message">{error}</p>;

    return (
        <div className="content-container">
            <h2>የግብይት ታሪክ (Transaction History)</h2>
            <div className="table-container">
                <table>
                    <thead>
                        <tr>
                            <th>Date & Time</th>
                            <th>ዓይነት (Type)</th>
                            <th>መጠን (Amount)</th>
                            <th>ቀሪ ሒሳብ (Running Balance)</th>
                            <th>Notes</th>
                        </tr>
                    </thead>
                    <tbody>
                        {transactions.map((tx) => (
                            <tr key={tx.id}>
                                <td>{new Date(tx.timestamp).toLocaleString()}</td>
                                <td>{tx.transaction_type_display}</td>
                                <td className={tx.signed_amount > 0 ? 'text-credit' : 'text-debit'}>
                                    {tx.signed_amount > 0 ? '+' : ''}
                                    {formatCurrency(tx.signed_amount)}
                                </td>
                                <td>{formatCurrency(tx.balance_after_transaction)}</td>
                                <td>{tx.notes}</td>
                            </tr>
                        ))}
                         {transactions.length === 0 && (
                            <tr>
                                <td colSpan="5">ምንም ዓይነት ግብይት አልተገኘም (No transactions found).</td>
                            </tr>
                        )}
                    </tbody>
                </table>
            </div>
        </div>
    );
}

export default TransactionHistoryPage;