import { Navigate, Outlet, useLocation } from "react-router-dom";
import useAuth from "@/hooks/use-auth";

function PublicRoute() {
  const { isAuthenticated, isLoading } = useAuth();
  const location = useLocation();

  if (isLoading) {
    return (
      <main className="flex min-h-screen items-center justify-center">
        <p className="text-gray-600">Checking authentication...</p>
      </main>
    );
  }

  if (isAuthenticated) {
    const destination = location.state?.from?.pathname ?? "/";

    return <Navigate to={destination} replace />;
  }

  return <Outlet />;
}

export default PublicRoute;
