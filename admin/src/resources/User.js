import * as React from "react";
import { List, Datagrid, TextField } from 'react-admin';
import pdfExporter from '../PdfExporter'
import moment from 'moment'

const userExporter = (users) => {
    const fields = ['Id', 'Servidor', 'Ativo', 'Criado em']
    const data = users.map(user => [user.id, user.server_id, user.active ? 'sim': 'não', moment(user.createdAt).format('DD/MM/YYYY')])

    pdfExporter('relatório_usuários.pdf', fields, data, 'Relatório de Usuários')
}

export const UserList = (props) => (
    <List {...props} exporter={userExporter}>
        <Datagrid>
            <TextField source="id" />
            <TextField source="server_id" label="Servidor"/>
            <TextField source="conn_id" label="Conexão"/>
            <TextField source="active" label="Ativo"/>
        </Datagrid>
    </List>
);

export const UserTitle = ({ record }) => {
    return <span>User {record ? `"${record.name}"` : ''}</span>;
};