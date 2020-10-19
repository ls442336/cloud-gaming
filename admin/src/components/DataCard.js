import * as React from "react";
import { Box, Card, CardContent, makeStyles, Typography } from '@material-ui/core';

const useStyles = makeStyles({
  root: {
    textAlign: 'center',
  },
  pos: {
    fontSize: 50,
  },
});

const DataCard = ({ title, description, color }) => {
  const classes = useStyles();

  return (
    <Box className={classes.root} border={1} borderColor={color || '#666666'}>
      <CardContent>
        <Typography className={classes.pos} color="textSecondary">
          {title}
        </Typography>
        <Typography variant="body2" component="p">
          {description}
        </Typography>
      </CardContent>
    </Box>
  )
}

export default DataCard;