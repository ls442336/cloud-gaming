import * as React from "react";
import { List, Datagrid, TextField } from 'react-admin';
import pdfExporter from '../PdfExporter'
import moment from 'moment'

const instanceExporter = (instances) => {
    const fields = ['Id', 'Servidor', 'Ativo', 'Criado em']
    const data = instances.map(instance => [instance.id, instance.server_id, instance.active ? 'sim': 'não', moment(instance.createdAt).format('DD/MM/YYYY')])

    pdfExporter('relatório_instâncias.pdf', fields, data, 'Relatório de Instâncias')
}

export const InstanceList = (props) => (
    <List {...props} exporter={instanceExporter}>
        <Datagrid>
            <TextField source="id" />
            <TextField source="server_id" label="Servidor"/>
            <TextField source="conn_id" label="Conexão"/>
            <TextField source="ready" />
            <TextField source="active" label="Ativo"/>
        </Datagrid>
    </List>
);

export const InstanceTitle = ({ record }) => {
    return <span>Instância {record ? `"${record.name}"` : ''}</span>;
};