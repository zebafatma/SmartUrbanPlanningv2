import { NavLink } from "react-router-dom";
import "./Navbar.css";

function Navbar() {
  return (
    <header className="navbar">
      <div className="navbar-container">

        {/* Logo */}

        <NavLink
          to="/"
          className="navbar-logo"
        >
          <span className="logo-mark">
            🌿
          </span>

          <span className="logo-name">
            Smart Urban
            <span>Planning</span>
          </span>
        </NavLink>


        {/* Navigation */}

        <nav className="navbar-links">

          <NavLink
            to="/"
            className={({ isActive }) =>
              isActive
                ? "nav-link active"
                : "nav-link"
            }
          >
            Home
          </NavLink>

          <NavLink
            to="/analysis"
            className={({ isActive }) =>
              isActive
                ? "nav-link active"
                : "nav-link"
            }
          >
            Analysis
          </NavLink>

          <NavLink
            to="/dashboard"
            className={({ isActive }) =>
              isActive
                ? "nav-link active"
                : "nav-link"
            }
          >
            Dashboard
          </NavLink>

          <NavLink
            to="/recommendations"
            className={({ isActive }) =>
              isActive
                ? "nav-link active"
                : "nav-link"
            }
          >
            Recommendations
          </NavLink>

        </nav>


        {/* Primary Action */}

        <NavLink
          to="/analysis"
          className="navbar-action"
        >
          Analyze
          <span>→</span>
        </NavLink>

      </div>
    </header>
  );
}

export default Navbar;