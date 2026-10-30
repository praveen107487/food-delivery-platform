import { isRouteErrorResponse, Link, useRouteError } from "react-router-dom";

function ErrorLayout() {
  const error = useRouteError();

  let title = "Something went wrong";
  let message = "An unexpected error occurred. Please try again.";

  if (isRouteErrorResponse(error)) {
    if (error.status === 404) {
      title = "Page Not Found";
      message = "The page you are looking for does not exist.";
    } else if (error.status === 403) {
      title = "Access Denied";
      message = "You do not have permission to access this page.";
    } else if (error.status === 401) {
      title = "Authentication Required";
      message = "Please log in to access this resource.";
    }
  }

  return (
    <main className="flex min-h-screen flex-col items-center justify-center gap-4 p-6 text-center">
      <h1 className="text-3xl font-bold">{title}</h1>

      <p className="text-gray-600">{message}</p>

      <Link
        to="/"
        className="rounded-md bg-green-600 px-5 py-2 text-white hover:bg-green-700"
      >
        Back to Home
      </Link>
    </main>
  );
}

export default ErrorLayout;
