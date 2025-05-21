'use client'

import React from 'react'

export default function Error({
                                  error,
                                  reset,
                              }: {
    error: Error
    reset: () => void
}) {
    return (
        <div style={{ padding: '2rem', textAlign: 'center' }}>
            <h2>出错了！</h2>
            <p>{error.message}</p>
            <button
                onClick={() => reset()}
                style={{ marginTop: '1rem', padding: '0.5rem 1rem' }}
            >
                重试
            </button>
        </div>
    )
}
