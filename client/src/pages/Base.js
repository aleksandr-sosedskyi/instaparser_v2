import React, { useState, useEffect } from "react";
import useStyles from './styles';
import MaterialTable from 'material-table';
import { Link } from "react-router-dom";
import { HOME } from "../constants/routes";
import { connect } from "react-redux";
import { getHackableUsers, changeUserStatus, getUsersWithSecret } from '../store/actions/users';
import { HACKABLE, UNHACKABLE, HACKED } from "../constants/general";


const Base = (props) => {

    const getUsersState = (data) => {
        return {
            columns: [
                { 
                    title: 'Username', 
                    field: 'username' ,
                    render: rowData => <a href={`https://instagram.com/${rowData.username}`} target='_blank'>{rowData.username}</a>
                },
                { 
                    title: 'E-mail', 
                    field: 'email',
                    render: rowData => (
                        <span  
                        className={classes.userEmail}
                        onClick={() => {navigator.clipboard.writeText(rowData.email)}}
                        >
                            {rowData.email}
                        </span>
                    )
                },
                { 
                    title: 'Subscribers', 
                    field: 'subscribers', 
                    type: 'numeric' 
                },
                {
                    title: 'pk', 
                    field: 'pk',
                }
            ],
            data: data
        }
    }

    const classes = useStyles();
    const [rightEmailUsersState, setRightEmailUsersState] = useState(getUsersState(props.rightEmailUsers));
    const [usersWithSecretState, setUsersWithSecretState] = useState(getUsersState(props.usersWithSecret));

    if (rightEmailUsersState.data.length == 0 && props.rightEmailUsers.length != 0 ){
        setRightEmailUsersState(getUsersState(props.rightEmailUsers));
    }

    if (usersWithSecretState.data.length == 0 && props.usersWithSecret.length != 0){
        setUsersWithSecretState(getUsersState(props.usersWithSecret))
    }

    const refreshRightEmailUsers = (pk) => {
        var new_data = JSON.parse(JSON.stringify(props.rightEmailUsers)).filter(user => user.pk != pk);
        setRightEmailUsersState(getUsersState(new_data));
    }

    const refreshUsersWithSecret = (pk) => {
        var new_data = JSON.parse(JSON.stringify(props.usersWithSecret)).filter(user => user.pk != pk);
        setUsersWithSecretState(getUsersState(new_data));
    }

    useEffect(() => {
        props.getHackableUsers();
        props.getUsersWithSecret();
    }, [props.rightEmailUsers.join(','), props.usersWithSecret.join(',')])

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
                    title="Hackable users"
                    columns={rightEmailUsersState.columns}
                    data={rightEmailUsersState.data}
                    actions={[
                        {
                            icon: 'done',
                            tooltip: 'Good User',
                            onClick: (event, rowData) => {
                                props.changeUserStatus(HACKABLE, rowData.pk);    
                                refreshRightEmailUsers(rowData.pk);
                            }
                        },
                        {
                            icon: 'close',
                            tooltip: 'Delete User',
                            onClick: (event, rowData) => {
                                props.changeUserStatus(UNHACKABLE, rowData.pk);
                                refreshRightEmailUsers(rowData.pk)
                            }
                        }
                    ]}
                    />
                </div>
                <div className={classes.withSecret}>
                <MaterialTable
                    title="Users with secret"
                    columns={usersWithSecretState.columns}
                    data={usersWithSecretState.data}
                    actions={[
                        {
                            icon: 'done',
                            tooltip: 'Good User',
                            onClick: (event, rowData) => {
                                props.changeUserStatus(HACKED, rowData.pk);    
                                refreshUsersWithSecret(rowData.pk);
                            }
                        },
                        {
                            icon: 'close',
                            tooltip: 'Delete User',
                            onClick: (event, rowData) => {
                                props.changeUserStatus(UNHACKABLE, rowData.pk);
                                refreshUsersWithSecret(rowData.pk)
                            }
                        }
                    ]}
                    />
                </div>
            </div>
        </>
    )
}

const mapStateToProps = (state) => ({
    rightEmailUsers: state.hackableUsers.users,
    usersWithSecret: state.usersWithSecret.users
})

export default connect(
    mapStateToProps,
    {
        getHackableUsers,
        changeUserStatus,
        getUsersWithSecret
    }
)(Base);