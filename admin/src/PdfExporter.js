import jsPDF from 'jspdf'
import 'jspdf-autotable'
import moment from 'moment'

const pdfExporter = (filename, fields, data, title) => {
    const doc = new jsPDF()

    doc.text(title + ` (${moment().format('DD/MM/YYYY')})`, doc.internal.pageSize.width / 2, 15, null, null, 'center');
    doc.setFontSize(14);
    doc.text('Cloud Gaming Platform', doc.internal.pageSize.width / 2, 25, null, null, 'center');

    doc.autoTable({
        head: [fields],
        body: data,
        margin: {vertical: 34}
    })

    doc.save(filename)
}

export default pdfExporter