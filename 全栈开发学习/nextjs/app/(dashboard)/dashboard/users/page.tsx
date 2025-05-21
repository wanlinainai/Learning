import Link from "next/link";

const Page = () => {
    return (
        <div>
            <h1>DashBoard Users</h1>

            <ul className="mt-10">
                <li>
                    <Link href="/app/(dashboard)/dashboard/users/1">User 1</Link>
                </li>
                <li>
                    <Link href="/app/(dashboard)/dashboard/users/2">User 2</Link>
                </li>
                <li>
                    <Link href="/app/(dashboard)/dashboard/users/3">User 3</Link>
                </li>
            </ul>
        </div>
    )
}

export default Page