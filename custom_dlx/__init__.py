import logging


class Node:
    def __init__(self, x, y, up=None, dw=None, lf=None, rg=None, uph=None, lfh=None):
        self.up = up if up else self
        self.dw = dw if dw else self
        self.lf = lf if lf else self
        self.rg = rg if rg else self
        self.uph = uph if uph else self
        self.lfh = lfh if lfh else self
        self.x = x
        self.y = y
        self.counter = 0

    def __repr__(self) -> str:
        data = '(x={};y={})'.format(self.x, self.y)
        if self.counter:
            data += '({})'.format(self.counter)
        return data


class DLX:
    """
    As a result, it returns an array of matrix row numbers that cover the condition
    """

    def __init__(self, source, dev=False):
        self.dev = dev
        self.buff = []
        self.__init_logger(self.dev)
        self.matrix = source
        self.links_head = Node(-1, -1)
        self.__generate_headers()
        self.__fill_main_linked_list(*self.__generate_nodes_lists())
        self.__dict_of_deleted_nodes = {}

    def solves(self):
        end = False
        while True:
            logging.debug(len(self.buff))
            selected_up_header = self.__select_up_header() if not end else None
            if selected_up_header:
                node = selected_up_header.dw
                self.buff.append(node)
                self.__cross_del(node)
            else:
                # yield [x.x for x in self.buff]
                if not self.buff and end:
                    break
                if self.links_head.rg == self.links_head:
                    yield [x.x for x in self.buff]
                node = self.buff.pop()
                self.__cross_restore(node)
                node = node.dw
                if node != node.uph:
                    self.buff.append(node)
                    self.__cross_del(node)
                    end = False
                else:
                    end = True

    def __cross_del(self, node: Node):
        up_headers_list = []
        head = node.lfh.rg
        while head != head.lfh:
            up_headers_list.append(head.uph.dw)
            head = head.rg
        left_headers_list = []
        for head in up_headers_list:
            while head != head.uph:
                left_headers_list.append(head.lfh.rg)
                head = head.dw
        left_headers_list = list(dict.fromkeys(left_headers_list))
        self.__dict_of_deleted_nodes[node] = left_headers_list
        for head in left_headers_list:
            while head != head.lfh:
                self.__del_node_from_horizontal_link(head)
                head = head.rg
        for head in up_headers_list:
            self.__del_node_from_vertical_link(head.uph)

    @staticmethod
    def __del_node_from_vertical_link(node: Node):
        lf_node = node.lf
        rg_node = node.rg
        lf_node.rg, rg_node.lf = rg_node, lf_node

    @staticmethod
    def __del_node_from_horizontal_link(node: Node):
        up_node = node.up
        dw_node = node.dw
        up_node.dw, dw_node.up = dw_node, up_node
        node.uph.counter -= 1

    def __cross_restore(self, node: Node):
        up_headers_list = []
        head = node.lfh.rg
        while head != head.lfh:
            up_headers_list.append(head.uph.dw)
            head = head.rg
        left_headers_list = self.__dict_of_deleted_nodes[node]
        for head in left_headers_list:
            while head != head.lfh:
                self.__restore_node_from_horizontal_link(head)
                head = head.rg
        del self.__dict_of_deleted_nodes[node]
        for head in up_headers_list:
            self.__restore_node_from_vertical_link(head.uph)

    @staticmethod
    def __restore_node_from_vertical_link(node: Node):
        lf_node = node.lf
        rg_node = node.rg
        lf_node.rg, rg_node.lf = node, node

    @staticmethod
    def __restore_node_from_horizontal_link(node: Node):
        up_node = node.up
        dw_node = node.dw
        up_node.dw, dw_node.up = node, node
        node.uph.counter += 1

    def __select_up_header(self):
        head = selected = self.links_head.rg
        while selected.counter and head != self.links_head:
            if head.counter < selected.counter:
                selected = head
            head = head.rg
        logging.debug(self.__debug_linked_list_header())
        # logging.debug(selected)
        return selected if (selected != self.links_head and selected.counter) else None

    def __generate_headers(self):
        self.__generate_left_headers()
        self.__generate_up_headers()

    def __generate_left_headers(self):
        for x, data in enumerate(self.matrix):
            if True in data:
                self.__add_down_node(self.links_head, Node(x, 0))

    def __generate_up_headers(self):
        for y in range(self.matrix.shape[1]):
            self.__add_right_node(self.links_head, Node(0, y))

    @staticmethod
    def __add_down_node(node1: Node, node2: Node):
        node2.uph = node1.uph
        node3 = node1.dw
        node2.up, node2.dw = node1, node3
        node1.dw = node3.up = node2

    @staticmethod
    def __add_right_node(node1: Node, node2: Node):
        node2.lfh = node1.lfh
        node3 = node1.rg
        node2.lf, node2.rg = node1, node3
        node1.rg = node3.lf = node2

    @staticmethod
    def __init_logger(developer_mode: bool):
        log_level = logging.INFO
        if developer_mode:
            log_level = logging.DEBUG
        logging.basicConfig(filename='dlx.log', level=log_level, filemode='w',
                            format='%(message)s', datefmt='%H:%M:%S')

    def __debug_linked_list(self):
        if self.dev:
            head1 = self.links_head
            while True:
                head2 = head1
                output = []
                while True:
                    output.append(str(head2))
                    head2 = head2.rg
                    if head2 == head1:
                        break
                logging.debug("".join(output))
                head1 = head1.dw
                if head1 == self.links_head:
                    break

    def __debug_linked_list_header(self):
        data = []
        head = self.links_head.rg
        while head != head.lfh:
            data.append(str(head))
            head = head.rg
        logging.debug(''.join(data))

    def __fill_main_linked_list(self, horizontal: dict, vertical: dict):
        # ?????????? ??????????, ?????????? ????????????????????
        head = self.links_head.dw
        while head != self.links_head:
            list_of_nodes = horizontal[head.x]
            for node in list_of_nodes:
                self.__add_right_node(head, node)
            head = head.dw
        head = self.links_head.rg
        while head != self.links_head:
            list_of_nodes = vertical[head.y]
            head.counter = len(list_of_nodes)
            for node in list_of_nodes:
                self.__add_down_node(head, node)
            head = head.rg

    def __generate_nodes_lists(self):
        # ?????????????? ?????????????? ?????????? ?????????????????? ?????????????????????????? ?? ??????????????????????
        vertical = {}
        horizontal = {}
        for y in range(self.matrix.shape[1]):
            vertical[y] = []
        for x, line in enumerate(self.matrix):
            for y, value in enumerate(line):
                if value:
                    node = Node(x, y)
                    vertical[y].append(node)
                    horizontal.setdefault(x, [])
                    horizontal[x].append(node)
        return horizontal, vertical
