import Link from "next/link";

const Page = () => {
    return  (
        <div>
            <h1>DashBoard Users</h1>

            <ul className="mt-10">
                <li>
                    <Link href="/dashboard/users/1">User 1</Link>
                </li>
                <li>User 2</li>
                <li>User 3</li>
                <li>User 4</li>
                <li>User 5</li>
            </ul>
        </div>
    )
}

export default Page