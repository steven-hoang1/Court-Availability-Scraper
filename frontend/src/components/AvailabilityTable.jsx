import { Table } from "@chakra-ui/react"

const AvailabilityTable = ({ data }) => {
  // Group by date, then by time
  const timeSet = new Set();
  const dateMap = {};

  data.forEach(({ date, time, courts_available }) => {
    if (!dateMap[date]) dateMap[date] = {};
    dateMap[date][time] = courts_available;
    timeSet.add(time);
  });

  const formatDate = (dateStr) => {
  const date = new Date(dateStr);
  return date.toLocaleDateString('en-AU', {
    weekday: 'short',
    day: 'numeric',
  }); 
};

  const times = Array.from(timeSet).sort();
  const dates = Object.keys(dateMap).sort();
  const formattedDates = dates.map(formatDate);

  return (
     <Table.ScrollArea borderWidth="1px" maxW="2xl" maxH="700px">
        <Table.Root stickyHeader={true} size="lg"  minW="600px">
        <Table.Header>
            <Table.Row bg="green.600">
            <Table.ColumnHeader textAlign="center">Time</Table.ColumnHeader>
            {formattedDates.map((date) => (
                <Table.ColumnHeader key={date} textAlign="center" py={2}>{date}</Table.ColumnHeader>
            ))}
            </Table.Row>
        </Table.Header>
        <Table.Body>
            {times.map((time) => (
            <Table.Row key={time} _hover={{ bg: "gray.100" }}>
                <Table.Cell fontWeight="bold" textAlign="center" py={1}>{time}</Table.Cell>
                {dates.map((date) => (
                <Table.Cell key={date} textAlign="center">
                    {dateMap[date]?.[time] ?? '-'}
                </Table.Cell>
                ))}
            </Table.Row>
            ))}
        </Table.Body>
        </Table.Root>
    </Table.ScrollArea>
    );
};

export default AvailabilityTable;