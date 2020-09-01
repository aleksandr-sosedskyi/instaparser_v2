import React, { useState } from "react";
import useStyles from './styles';
import MaterialTable from 'material-table';
import { Link } from "react-router-dom";
import { HOME } from "../constants/routes";


const Base = (props) => {
    const classes = useStyles();
    return (
        <>
            <header className={classes.header}>
                <h5>
                    <Link to={HOME}>Instaparser</Link>
                </h5>
                <div className={classes.tabsDiv}>
                    <p>Для взлома</p>
                    <p>С секретным вопросом</p>
                </div>
            </header>
            <div className={classes.mainBlock}>
                <div className={classes.forHack}>
                    <div class="container">
                        <div class="row">
                            <div class="col-12">
                            <table class="table table-bordered">
                                <thead>
                                <tr>
                                    <th scope="col">Day</th>
                                    <th scope="col">Article Name</th>
                                    <th scope="col">Author</th>
                                    <th scope="col">Shares</th>
                                    <th scope="col">Actions</th>
                                </tr>
                                </thead>
                                <tbody>
                                <tr>
                                    <th scope="row">1</th>
                                    <td>Bootstrap 4 CDN and Starter Template</td>
                                    <td>Cristina</td>
                                    <td>2.846</td>
                                    <td>
                                    <button type="button" class="btn btn-primary"><i class="far fa-eye"></i></button>
                                    <button type="button" class="btn btn-success"><i class="fas fa-edit"></i></button>
                                    <button type="button" class="btn btn-danger"><i class="far fa-trash-alt"></i></button>
                                    </td>
                                </tr>
                                <tr>
                                    <th scope="row">2</th>
                                    <td>Bootstrap Grid 4 Tutorial and Examples</td>
                                    <td>Cristina</td>
                                    <td>3.417</td>
                                    <td>
                                    <button type="button" class="btn btn-primary"><i class="far fa-eye"></i></button>
                                    <button type="button" class="btn btn-success"><i class="fas fa-edit"></i></button>
                                    <button type="button" class="btn btn-danger"><i class="far fa-trash-alt"></i></button>
                                    </td>
                                </tr>
                                <tr>
                                    <th scope="row">3</th>
                                    <td>Bootstrap Flexbox Tutorial and Examples</td>
                                    <td>Cristina</td>
                                    <td>1.234</td>
                                    <td>
                                    <button type="button" class="btn btn-primary"><i class="far fa-eye"></i></button>
                                    <button type="button" class="btn btn-success"><i class="fas fa-edit"></i></button>
                                    <button type="button" class="btn btn-danger"><i class="far fa-trash-alt"></i></button>
                                    </td>
                                </tr>
                                </tbody>
                            </table>
                            </div>
                        </div>
                    </div>
                </div>
                <div className={classes.withSecret}>

                </div>
            </div>
        </>
    )
}

export default Base;