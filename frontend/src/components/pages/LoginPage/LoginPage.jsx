import { useLocation, useNavigate } from "react-router-dom"; 
import { useAuth } from "../../../hooks/useAuth";
import { getToken } from "../../../api/api";

const LoginPage = () => {
    const navigate = useNavigate();
    const location = useLocation();
    const { onLogin } = useAuth();

    const fromPage = location.state?.from?.pathname || '/';

    const handleSubmit = (e) => {
        e.preventDefault();
        const form = e.target;
        const auth = {
            username: form.username.value,
            password: form.password.value
        }
        getToken(auth)
        .then(response => {
            if (response.ok) {
                return response.json()
            }
            throw new Error("401 Unauthorized!")
        })
        .then(result => onLogin(result, () => navigate(fromPage, {replace: true})))
    }
    return (
        <div>
           <form onSubmit={ handleSubmit }>
            <label htmlFor="username">Username</label>
            <input type="text" name="username" id="usename" />
            <label htmlFor="password">Password</label>
            <input type="password" name="password" id="password" />
            <button type="submit">Login</button>
           </form> 
        </div>
    );
};

export default LoginPage;