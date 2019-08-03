import React from 'react';
import './NoMatch.css';
import {Link as RouterLink} from "react-router-dom";
import Link from "@material-ui/core/Link";

function NoMatch() {
    return (
        <div className="NoMatch">
            <Link component={RouterLink} to="/">
                Sorry, this page doesn't exist. Click Here to Go Back Home.
            </Link>
        </div>
    );
}

export default NoMatch;