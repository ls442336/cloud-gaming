import * as React from "react";
import { List, Datagrid, TextField } from 'react-admin';
import pdfExporter from '../PdfExporter'
import moment from 'moment'

const sessionExporter = (sessions) => {
    const fields = ['Id', 'Jogo', 'Usuário', 'Instância', 'Servidor', 'Status', 'Criado em']
    const data = sessions.map(session => [session.id, session.game, session.user,
    session.instance, session.server_id, session.status, moment(session.createdAt).format('DD/MM/YYYY')])

    pdfExporter('relatório_sessões.pdf', fields, data, 'Relatório de Sessões')
}

export const SessionList = (props) => (
    <List {...props} exporter={sessionExporter}>
        <Datagrid>
            <TextField source="game" label="Jogo"/>
            <TextField source="user" label="Usuário"/>
            <TextField source="instance" label="Instância"/>
            <TextField source="server_id" label="Servidor"/>
            <TextField source="status"/>
            <TextField source="active" label="Ativo"/>
            
        </Datagrid>
    </List>
);