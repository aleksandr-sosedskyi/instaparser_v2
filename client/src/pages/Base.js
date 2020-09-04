import React, { useState, useEffect } from "react";
import useStyles from './styles';
import MaterialTable from 'material-table';
import { Link } from "react-router-dom";
import { HOME } from "../constants/routes";
import { TablePagination } from '@material-ui/core';
import { connect } from "react-redux";
import { getHackableUsers, changeUserStatus } from '../store/actions/users';
import { HACKABLE, UNHACKABLE } from "../constants/general";


const Base = (props) => {
    const getUsersState = (data) => {
        return {
            columns: [
                { 
                    title: 'Username', 
                    field: 'username' ,
                    render: rowData => <a href={`https://instagram.com/${rowData.username}`} target='_blank'>{rowData.username}</a>
                },
                { title: 'E-mail', field: 'email'},
                { title: 'Subscribers', field: 'subscribers', type: 'numeric' },
                {title: 'pk', field: 'pk',}
            ],
            data: data
        }
    }

    const classes = useStyles();
    const [state, setState] = useState(getUsersState(props.users));

    if (state.data.length == 0 && props.users.length != 0){
        setState(getUsersState(props.users));
    }

    useEffect(() => {
        props.getHackableUsers();
    }, [props.users.join(',')])

    return (
        <>
            <header className={classes.header}>
                <h5>
                    <Link to={HOME}>PET</Link>
                </h5>
                <div className={classes.tabsDiv}>
                    <p>1</p>
                    <p>2</p>
                </div>
            </header>
            <div className={classes.mainBlock}>
                <div className={classes.forHack}>
                    <MaterialTable
                    title="Editable Example"
                    columns={state.columns}
                    data={state.data}
                    actions={[
                        {
                            icon: 'done',
                            tooltip: 'Good User',
                            onClick: (event, rowData) => {
                                changeUserStatus(HACKABLE, rowData.pk)
                            }
                        },
                        {
                            icon: 'close',
                            tooltip: 'Delete User',
                            onClick: (event, rowData) => {
                                console.log(event);
                                console.log(rowData);
                            }
                        }
                    ]}
                    />
                </div>
                <div className={classes.withSecret}>

                </div>
            </div>
        </>
    )
}

const mapStateToProps = (state) => ({
    users: state.hackableUsers.users
})

export default connect(
    mapStateToProps,
    {
        getHackableUsers,
        changeUserStatus
    }
)(Base);