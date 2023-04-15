import { useLocation, Navigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';

const ProtectedRouter = ({children}) => {
    const location = useLocation();
    const { token } = useAuth();

    if (!token) {
        return <Navigate  to="/login" replace state={{from: location}} />
    }

    return children;
}

export {ProtectedRouter};
