'use client'
export default function GlobalError({error}: {error: Error & {digest?: string}}) {
    return (
        <div>
            <body>
                <h1>{error.message}</h1>
            </body>
        </div>
    )
}